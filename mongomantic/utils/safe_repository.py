"""SafeRepository is a subclass of BaseRepository that handles all raised errors
"""

from typing import Dict, Iterator, List, Type

from mongomantic.config import logger
from mongomantic.core.base_repository import BaseRepository
from mongomantic.core.errors import DoesNotExistError, InvalidQueryError, MultipleObjectsReturnedError, WriteError
from mongomantic.core.mongo_model import MongoDBModel


class SafeRepository(BaseRepository):
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
    def save(cls, model) -> Type[MongoDBModel]:
        try:
            return super().save(model)
        except WriteError as e:
            logger.error(e)
            return None

    @classmethod
    def get(cls, **kwargs) -> Type[MongoDBModel]:
        try:
            return super().get(**kwargs)
        except (DoesNotExistError, MultipleObjectsReturnedError) as e:
            logger.error(e)
            return None

    @classmethod
    def find(cls, **kwargs) -> Iterator[Type[MongoDBModel]]:
        try:
            gen = super().find(**kwargs)
            try:
                yield from gen
            except InvalidQueryError as e:
                logger.error(e)
                return None

        except InvalidQueryError as e:
            logger.error(e)
            return None

    @classmethod
    def aggregate(cls, pipeline: List[Dict]):
        try:
            gen = super().aggregate(pipeline)
            try:
                yield from gen
            except InvalidQueryError as e:
                logger.error(e)
                return None

        except InvalidQueryError as e:
            logger.error(e)
            return None
