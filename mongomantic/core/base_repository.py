from typing import Any, Dict, Iterator, List, Tuple, Type

from abc import ABCMeta

from bson import ObjectId
from bson.objectid import InvalidId
from mongomantic.core.index import Index
from pymongo.collection import Collection

from .database import MongomanticClient
from .errors import (
    DoesNotExistError,
    FieldDoesNotExistError,
    IndexCreationError,
    InvalidQueryError,
    MultipleObjectsReturnedError,
    WriteError,
)
from .mongo_model import MongoDBModel


class ABRepositoryMeta(ABCMeta):
    """Abstract Base Repository Metaclass

    This Metaclass ensures that any concrete implementations of BaseRepository
    include all necessary definitions, in order to decrease user errors.
    """

    def __new__(cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any], **kwds: Any):
        base_repo = super().__new__(cls, name, bases, namespace, **kwds)
        meta = base_repo.__dict__.get("Meta", False)
        if not meta:
            raise NotImplementedError("Internal 'Meta' not implemented")
        # Check existence of model and collection
        if not (meta.__dict__.get("model", False) and meta.__dict__.get("collection", False)):
            raise NotImplementedError("'model' or 'collection' properties are missing from internal Meta class")

        return base_repo


class BaseRepository(metaclass=ABRepositoryMeta):
    class Meta:
        @property
        def model(self) -> Type[MongoDBModel]:
            """Model class that subclasses MongoDBModel"""
            raise NotImplementedError

        @property
        def collection(self) -> str:
            """String representing the MongoDB collection to use when storing this model"""
            raise NotImplementedError

        @property
        def indexes(self) -> List[Index]:
            """List of MongoDB indexes that should be setup for this particular model"""
            raise NotImplementedError

    @classmethod
    def _get_collection(cls) -> Collection:
        """Returns a reference to the MongoDB collection, and initializes indexes if first time"""
        if not hasattr(cls, "_indexes") or cls._indexes is None:
            cls._indexes = True  # State to know that already checked

            if getattr(cls.Meta, "auto_create_index", True):
                cls._create_indexes()

        return MongomanticClient.db.__getattr__(cls.Meta.collection)

    @classmethod
    def _create_indexes(cls):
        indexes = getattr(cls.Meta, "indexes", False)
        if indexes:
            try:
                pymongo_indexes = [index.to_pymongo() for index in indexes]
                cls._get_collection().create_indexes(pymongo_indexes)
            except Exception as e:
                raise IndexCreationError(f"Failed to create indexes: {e}")

    @classmethod
    def _process_kwargs(cls, kwargs: Dict) -> Tuple:
        """Update keyword arguments from human readable to mongo specific"""
        if "id" in kwargs:
            try:
                oid = str(kwargs.pop("id"))
                oid = ObjectId(oid)
                kwargs["_id"] = oid
            except InvalidId:
                raise InvalidQueryError(f"Invalid ObjectId {oid}.")

        projection = kwargs.pop("projection", None)
        skip = kwargs.pop("skip", 0)
        limit = kwargs.pop("limit", 0)

        for key in kwargs:
            if key not in cls.Meta.model.__fields__:
                raise FieldDoesNotExistError(f"Field {key} does not exist for model {cls.Meta.model}")

        return projection, skip, limit

    @classmethod
    def save(cls, model) -> Type[MongoDBModel]:
        """Saves object in MongoDB"""
        try:
            document = model.to_mongo()
            res = cls._get_collection().insert_one(document)
        except Exception as e:
            raise WriteError(f"Error inserting document: \n{e}")

        document["_id"] = res.inserted_id
        return cls.Meta.model.from_mongo(document)

    @classmethod
    def get(cls, **kwargs) -> Type[MongoDBModel]:
        """Get a unique document based on some filter.

        Args:
            kwargs: Filter keyword arguments

        Raises:
            DoesNotExistError: If object not found
            MultipleObjectsReturnedError: If more than one object matches filter

        Returns:
            Type[MongoDBModel]: Matching model
        """
        cls._process_kwargs(kwargs)

        try:
            res = cls._get_collection().find(filter=kwargs, limit=2)
            document = next(res)
        except StopIteration:
            raise DoesNotExistError("Document not found")

        try:
            next(res)
            raise MultipleObjectsReturnedError("2 or more items returned, instead of 1")
        except StopIteration:
            return cls.Meta.model.from_mongo(document)

    @classmethod
    def find(cls, **kwargs) -> Iterator[Type[MongoDBModel]]:
        """Queries database and filters on kwargs provided.

        Args:
            kwargs: Filter keyword arguments

            Reserved *optional* field names:
            projection: can either be a list of field names that should be returned in the result set
                        or a dict specifying the fields to include or exclude. If projection is a list
                        “_id” will always be returned. Use a dict to exclude fields from the result
                        (e.g. projection={‘_id’: False}).
            skip: the number of documents to omit when returning results
            limit: the maximum number of results to return

        Note that invalid query errors may not be detected until the generator is consumed.
        This is because the query is not executed until the result is needed.

        Raises:
            InvalidQueryError: In case one or more arguments were invalid

        Yields:
            Iterator[Type[MongoDBModel]]: Generator that wraps PyMongo cursor and transforms documents to models
        """
        projection, skip, limit = cls._process_kwargs(kwargs)

        try:
            results = cls._get_collection().find(filter=kwargs, projection=projection, skip=skip, limit=limit)
            for result in results:
                yield cls.Meta.model.from_mongo(result)
        except Exception as e:
            raise InvalidQueryError(f"Invalid argument types: {e}")

    @classmethod
    def aggregate(cls, pipeline: List[Dict]):
        try:
            results = cls._get_collection().aggregate(pipeline)
            for result in results:
                yield cls.Meta.model.from_mongo(result)
        except Exception as e:
            raise InvalidQueryError(f"Error executing pipeline: {e}")
