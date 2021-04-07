from typing import Type, Union

from abc import ABC, abstractmethod

from bson import ObjectId
from bson.objectid import InvalidId
from mongomantic.config import logger

from .database import MongomanticClient
from .errors import DoesNotExistError, InvalidQueryError, MultipleObjectsReturnedError, WriteError
from .mongo_model import MongoDBModel


def process_kwargs(kwargs):
    """Update keyword arguments from human readable to mongo specific"""
    if "id" in kwargs:
        try:
            oid = str(kwargs.pop("id"))
            oid = ObjectId(oid)
            kwargs["_id"] = oid
        except InvalidId:
            raise InvalidQueryError(f"Invalid ObjectId {oid}.")


class BaseRepository(ABC):
    @property
    @abstractmethod
    def _model(self) -> Type[MongoDBModel]:
        pass

    @property
    @abstractmethod
    def _collection(self) -> str:
        """String representing the MongoDB collection to use when storing this model"""
        pass

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
                raise WriteError(f"Error inserting document")

        document["_id"] = res.inserted_id
        return self._model.from_mongo(document)

    def get(self, **kwargs) -> Type[MongoDBModel]:
        process_kwargs(kwargs)

        try:
            res = MongomanticClient.db.__getattr__(self._collection).find(filter=kwargs, limit=2)
            document = next(res)
        except StopIteration:
            raise DoesNotExistError(f"Document not found")

        try:
            res = next(res)
            raise MultipleObjectsReturnedError("2 or more items returned, instead of 1")
        except StopIteration:
            return self._model.from_mongo(document)

    # def objects(self, limit=None, skip=None, **kwargs) -> Type[MongoDBModel]:
    #     process_kwargs(kwargs)

    #     try:
    #         MongomanticClient.db.__getattr__(self._collection).find(filter=kwargs).limit(limit).skip(skip)
