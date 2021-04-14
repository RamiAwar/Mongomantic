from typing import Any, Dict, Optional, Type

from abc import ABC
from datetime import datetime

from bson import ObjectId
from bson.objectid import InvalidId
from pydantic import BaseConfig, BaseModel


class OID:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Invalid object ID")


class MongoDBModel(BaseModel, ABC):

    id: Optional[OID]

    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: str,
        }

    @classmethod
    def from_mongo(cls, data: Dict[str, Any]) -> Optional[Type["MongoDBModel"]]:
        """Constructs a pydantic object from mongodb compatible dictionary"""
        if not data:
            return None

        id = data.pop("_id", None)  # Convert _id into id
        return cls(**dict(data, id=id))

    def to_mongo(self, **kwargs):
        """Maps a pydantic model to a mongodb compatible dictionary"""

        exclude_unset = kwargs.pop(
            "exclude_unset",
            False,  # Set as false so that default values are also stored
        )

        by_alias = kwargs.pop(
            "by_alias", True
        )  # whether field aliases should be used as keys in the returned dictionary

        # Converting the model to a dictionnary
        parsed = self.dict(by_alias=by_alias, exclude_unset=exclude_unset, **kwargs)

        # Mongo uses `_id` as default key.
        # if "_id" not in parsed and "id" in parsed:
        #    parsed["_id"] = parsed.pop("id")

        if "id" in parsed:
            parsed.pop("id")

        return parsed

    def dict(self, **kwargs):
        """Override self.dict to hide some fields that are used as metadata"""
        hidden_fields = {"_collection"}
        kwargs.setdefault("exclude", hidden_fields)
        return super().dict(**kwargs)
