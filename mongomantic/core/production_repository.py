from typing import Type, Union

from abc import ABC, abstractmethod

from bson import ObjectId
from bson.objectid import InvalidId
from mongomantic.config import logger

from .base_repository import BaseRepository
from .database import db
from .mongo_model import MongoDBModel

# class ProductionRepository(BaseRepository):
#     def save(self, model):
#         """Saves current object in MongoDB"""

#         try:
#             res = super().save(model)
#         except Exception as e:
#             res = None
#             logger.error(f"Error on save: \n{e}")
#         else:
#             if res is None:
#                 logger.error("Error inserting document into MongoDB.")

#         document["_id"] = res.inserted_id
#         return self._model.from_mongo(document)

#     def get(self, oid: Union[str, ObjectId]):
#         try:
#             res = super().get(oid)
#         except InvalidId:
#             logger.error(f"Invalid ObjectId {oid}.")
#             return None

#         res = db[self._collection].find(filter={"_id": oid}, limit=2)

#         try:
#             document = next(res)
#         except StopIteration:
#             logger.error(f"Object {oid} not found.")

#         return self._model.from_mongo(document)

# @classmethod
# def get_count(cls, **predicate):
#     """Returns Objects count"""
#     return cls.schema_class.objects(**predicate).count()

# @classmethod
# def get(cls, forced: bool = True, **predicate):
#     """Uses predicates to get unique object. Logs error if object does not exist or is not unique."""
#     try:
#         obj = cls.schema_class.objects.get(**predicate)
#     except DoesNotExist as e:
#         obj = None
#         if forced:
#             loggers.database_logger.error(f"Get unique object failed: Object not found!: {e}")
#     except MultipleObjectsReturned as e:
#         obj = None
#         loggers.database_logger.error(f"Get unique object failed: Multiple objects returned!: {e}")

#     if obj:
#         return cls.from_mongo(obj.to_mongo(use_db_field=True))
#     else:
#         return None

# @classmethod
# def get_all(cls):
#     """Returns All Objects (QuerySet)"""
#     return cls.schema_class.objects

# @classmethod
# def get_unique_object(cls, id: str):
#     """Returns Object if exists or None"""
#     objects = cls.schema_class.objects(id=id)

#     if objects is None:
#         return None

#     first_object = objects.first()
#     if first_object is None:
#         return None

#     return cls.from_mongo(first_object.to_mongo(use_db_field=True))

# @classmethod
# def get_objects(cls, **predicate):
#     """Uses predicates"""
#     objects = cls.schema_class.objects(**predicate)
#     # TODO[PW] : Test this
#     # return (cls.from_mongo(object.to_mongo(use_db_field=True)) for object in objects)
#     return [cls.from_mongo(object.to_mongo(use_db_field=True)) for object in objects]

# @classmethod
# def search_by_text(cls, text: str, limit: int):
#     """Returns generator of objects matching text query"""
#     objects = cls.schema_class.objects.search_text(text).limit(limit)
#     return (cls.from_mongo(object.to_mongo(use_db_field=True)) for object in objects)

# @classmethod
# def get_custom_objects(cls, custom_cls, pipeline, **predicate):
#     """Uses predicates and pagination logic"""
#     query_set = cls.schema_class.objects(**predicate)
#     is_aggregate = False
#     if not pipeline:
#         pass
#     else:
#         is_aggregate = True
#         query_set = query_set.aggregate(*pipeline)

#     if custom_cls is None:
#         if is_aggregate:
#             return [
#                 cls.from_mongo(object) for object in query_set
#             ]  # since response from aggregate is a dict, not MongoModel

#         return [cls.from_mongo(object.to_mongo(use_db_field=True)) for object in query_set]
#     else:
#         return [custom_cls(**object) for object in query_set]

# @classmethod
# def get_max(cls, custom_cls, property_name: str, pipeline, **predicate):
#     """Uses predicates and pagination logic"""
#     query_set = cls.schema_class.objects(**predicate)
#     query_set = query_set.order_by(f"-{property_name}")
#     # query_set = query_set.limit(1) # do not actually need since below return first?
#     is_aggregate = False
#     if not pipeline:
#         pass
#     else:
#         is_aggregate = True
#         query_set = query_set.aggregate(*pipeline)

#     try:
#         query_set_object = query_set.next()
#     except StopIteration:
#         return None

#     if query_set_object is None:
#         return None

#     if custom_cls is None:
#         if is_aggregate:
#             return cls.from_mongo(query_set_object)  # since response from aggregate is a dict, not MongoModel

#         return cls.from_mongo(query_set_object.to_mongo(use_db_field=True))
#     else:
#         return custom_cls(**query_set_object)

# @classmethod
# def paginate_objects(cls, order_by: str, limit: int, **predicate):
#     """Uses predicates and pagination logic"""
#     query_set = cls.schema_class.objects(**predicate)
#     total_items = query_set.count()
#     if order_by is not None:
#         query_set = query_set.order_by(order_by)
#     if limit is not None:
#         query_set = query_set.limit(limit)
#     items = [cls.from_mongo(object.to_mongo(use_db_field=True)) for object in query_set]
#     has_more = total_items > (len(items))
#     return items, has_more

# @classmethod
# def paginate_custom_objects(cls, custom_cls, order_by: str, limit: int, pipeline, **predicate):
#     """Uses predicates and pagination logic"""
#     query_set = cls.schema_class.objects(**predicate)
#     total_items = query_set.count()
#     if order_by is not None:
#         query_set = query_set.order_by(order_by)
#     if limit is not None:
#         query_set = query_set.limit(limit)
#     query_set = query_set.aggregate(*pipeline)

#     items = [custom_cls.from_mongo(object) for object in query_set]
#     has_more = total_items > (len(items))
#     return items, has_more

# # 3. Update

# def update(self):
#     """Updates current object, must have an id!"""
#     return self.save()  # same as save, but here in case we want to modify somethings

# # 4. Delete

# @classmethod
# def delete_object(cls, id: str):
#     """Deletes Object with specified Id"""
#     mongo_object = cls.get_unique_object(id=id)

#     if mongo_object is None:
#         return id  # not found, so already deleted

#     if issubclass(cls, Syncable):
#         mongo_object.modified_at = datetime.now(timezone.utc)

#     if issubclass(cls, SoftDeletable):
#         mongo_object.deleted = True
#         saved_object = mongo_object.save()
#         return saved_object.id

#     try:
#         mongo_object.delete()
#         return id
#     except Exception as e:
#         logger.error("Error deleting model: " + str(e))
#         raise e

# def delete(self):
#     """Deletes current object"""
#     return self.delete_object(id=self.id)  # takes care of modified_at, etc...
