import datetime
from typing import Generic, List, TypeVar
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class Entity(BaseModel):
  id: str = Field(alias="_id", default=None)
  created_at: datetime.datetime = Field(default=None)
  updated_at: datetime.datetime = Field(default=None)

  @field_validator("id", mode="before")
  @classmethod
  def convert_id_to_str(cls, value):
    if isinstance(value, ObjectId):
      return str(value)
    return value

  def model_dump(self, *args, **kwargs):
    original_dict = super().model_dump(*args, **kwargs)
    if original_dict.get("_id"):
      original_dict["_id"] = ObjectId(original_dict["_id"])
    return original_dict

  def initialize(self):
    now = datetime.datetime.now(datetime.timezone.utc)
    self.id = str(ObjectId())
    self.created_at = now
    self.updated_at = now

  def on_update(self):
    now = datetime.datetime.now(datetime.timezone.utc)
    self.updated_at = now

  @classmethod
  def from_dict(cls, json_object: dict):
    return cls(**json_object)


T = TypeVar("T")


class PagedEntity(BaseModel, Generic[T]):
  total: int = Field(...)
  items: List[T] = Field(...)
