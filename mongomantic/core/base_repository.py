from typing import Dict, Iterator, List, Tuple, Type

from abc import ABC, abstractmethod

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


class BaseRepository(ABC):
    @property
    @abstractmethod
    def _model(self) -> Type[MongoDBModel]:
        raise NotImplementedError

    @property
    @abstractmethod
    def _collection(self) -> str:
        """String representing the MongoDB collection to use when storing this model"""
        raise NotImplementedError

    def process_kwargs(self, kwargs: Dict) -> Tuple:
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
            if key not in self._model.__fields__:
                raise FieldDoesNotExistError(f"Field {key} does not exist for model {self._model}")

        return projection, skip, limit

    def save(self, model) -> Type[MongoDBModel]:
        """Saves object in MongoDB"""
        try:
            document = model.to_mongo()
            res = MongomanticClient.db.__getattr__(self._collection).insert_one(document)
        except Exception as e:
            res = None
            raise WriteError(f"Error inserting document: \n{e}")
        else:
            if res is None:
                raise WriteError("Error inserting document")

        document["_id"] = res.inserted_id
        return self._model.from_mongo(document)

    def get(self, **kwargs) -> Type[MongoDBModel]:
        """Get a unique document based on some filter.

        Args:
            kwargs: Filter keyword arguments

        Raises:
            DoesNotExistError: If object not found
            MultipleObjectsReturnedError: If more than one object matches filter

        Returns:
            Type[MongoDBModel]: Matching model
        """
        self.process_kwargs(kwargs)

        try:
            res = MongomanticClient.db.__getattr__(self._collection).find(filter=kwargs, limit=2)
            document = next(res)
        except StopIteration:
            raise DoesNotExistError("Document not found")

        try:
            res = next(res)
            raise MultipleObjectsReturnedError("2 or more items returned, instead of 1")
        except StopIteration:
            return self._model.from_mongo(document)

    def find(self, **kwargs) -> Iterator[Type[MongoDBModel]]:
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
        projection, skip, limit = self.process_kwargs(kwargs)

        try:
            results = MongomanticClient.db.__getattr__(self._collection).find(
                filter=kwargs, projection=projection, skip=skip, limit=limit
            )
            for result in results:
                yield self._model.from_mongo(result)
        except Exception as e:
            raise InvalidQueryError(f"Invalid argument types: {e}")

    def aggregate(self, pipeline: List[Dict]):
        try:
            results = MongomanticClient.db.__getattr__(self._collection).aggregate(pipeline)
            for result in results:
                yield self._model.from_mongo(result)
        except Exception as e:
            raise InvalidQueryError(f"Error executing pipeline: {e}")
