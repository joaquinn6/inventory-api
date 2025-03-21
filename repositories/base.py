from typing import Generic, TypeVar, List, Callable
from bson import ObjectId
import pymongo
from pymongo.collection import Collection
from pymongo.typings import _DocumentType
from core import var_mongo_provider as mongo_provider
from models.entity import PagedEntity

T = TypeVar("T")


class RepositoryBase(Generic[T]):

  def __init__(self, collection: str, mapper: Callable) -> None:
    self._collection: Collection[_DocumentType] = mongo_provider.db.get_collection(
        collection)
    self._mapper = mapper

  def count(self, query: dict):
    return self._collection.count_documents(query)

  def get(self, query: dict,  sort: str = '', direction: int = pymongo.DESCENDING) -> List[T]:
    order = [('_id', pymongo.DESCENDING)]
    if sort:
      order = [(sort, direction)]
    cursor = self._collection.find(query).sort(order)
    return [self._mapper(entity) for entity in cursor]

  def get_one(self, query: dict) -> T | None:
    res = self._collection.find_one(query)
    if not res:
      return None
    return self._mapper(res)

  def get_by_id(self, identifier: str) -> T | None:
    res = self._collection.find_one({'_id': ObjectId(identifier)})
    if not res:
      return None
    return self._mapper(res)

  def get_paged(self, query: dict, page: int, limit: int, sort: str = '', direction: int = pymongo.DESCENDING) -> PagedEntity:
    total = self.count(query)
    order = [('_id', pymongo.DESCENDING)]
    if sort:
      order = [(sort, direction)]

    skips = 0
    if page > 1:
      skips = limit * (page - 1)

    cursor = self._collection.find(query).sort(
        order).skip(skips).limit(limit)
    return PagedEntity(total=total, items=[self._mapper(entity) for entity in cursor])

  def insert(self, entity: T):
    self._collection.insert_one(entity.model_dump(by_alias=True))

  def insert_many(self, entities: List[T]):
    entities_list = [entity.model_dump(by_alias=True) for entity in entities]
    self._collection.insert_many(entities_list)

  def update(self, query: dict, entity: T, upsert: bool = False):
    self._collection.update_one(
        query, {'$set': entity.model_dump(by_alias=True)}, upsert=upsert)

  def update_by_id(self, entity: T, upsert: bool = False):
    self._collection.update_one(
        {"_id": ObjectId(entity.id)}, {'$set': entity.model_dump(by_alias=True)}, upsert=upsert)

  def update_many(self, query: dict, update: dict):
    self._collection.update_many(query, {'$set': update})

  def delete_many(self, query):
    self._collection.delete_many(query)

  def delete_by_id(self, identifier: str):
    self._collection.delete_one({"_id": ObjectId(identifier)})

  def aggregate(self, pipeline: List) -> list | dict | None:
    return self._collection.aggregate(pipeline)
