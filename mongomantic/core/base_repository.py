from typing import Dict, Iterator, List, Tuple, Type

from abc import ABCMeta

from bson import ObjectId
from bson.objectid import InvalidId

from .database import MongomanticClient
from .errors import (
    DoesNotExistError,
    FieldDoesNotExistError,
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

    def __new__(cls, name, bases, dct):
        base_repo = super().__new__(cls, name, bases, dct)
        meta = base_repo.__dict__.get("Meta", False)
        if not meta:
            raise NotImplementedError("Internal 'Meta' not implemented")
        else:
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

    @classmethod
    def process_kwargs(cls, kwargs: Dict) -> Tuple:
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
            res = MongomanticClient.db.__getattr__(cls.Meta.collection).insert_one(document)
        except Exception as e:
            res = None
            raise WriteError(f"Error inserting document: \n{e}")
        else:
            if res is None:
                raise WriteError("Error inserting document")

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
        cls.process_kwargs(kwargs)

        try:
            res = MongomanticClient.db.__getattr__(cls.Meta.collection).find(filter=kwargs, limit=2)
            document = next(res)
        except StopIteration:
            raise DoesNotExistError("Document not found")

        try:
            res = next(res)
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
        projection, skip, limit = cls.process_kwargs(kwargs)

        try:
            results = MongomanticClient.db.__getattr__(cls.Meta.collection).find(
                filter=kwargs, projection=projection, skip=skip, limit=limit
            )
            for result in results:
                yield cls.Meta.model.from_mongo(result)
        except Exception as e:
            raise InvalidQueryError(f"Invalid argument types: {e}")

    @classmethod
    def aggregate(cls, pipeline: List[Dict]):
        try:
            results = MongomanticClient.db.__getattr__(cls.Meta.collection).aggregate(pipeline)
            for result in results:
                yield cls.Meta.model.from_mongo(result)
        except Exception as e:
            raise InvalidQueryError(f"Error executing pipeline: {e}")
