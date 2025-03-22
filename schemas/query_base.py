from enum import Enum
from pydantic import BaseModel, Field, field_validator
import pymongo


class OrderSort(int, Enum):
  ASCENDING = pymongo.ASCENDING
  DESCENDING = pymongo.DESCENDING


class QueryBase(BaseModel):
  page: int = Field(default=0)
  limit: int = Field(default=0)
  order: OrderSort = OrderSort.DESCENDING
  sort: str = Field(default='created_at')

  def get_pagination(self) -> dict:
    return {
        'page': self.page,
        'limit': self.limit,
        'order': self.order,
        'sort': self.sort
    }

  @field_validator("order", mode="before")
  @classmethod
  def order_parser(cls, value):
    if value == 'ascending':
      return OrderSort.ASCENDING
    return OrderSort.DESCENDING
