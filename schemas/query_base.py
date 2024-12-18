from enum import Enum
from pydantic import BaseModel, Field


class OrderSort(str, Enum):
  ASCENDING = "ascending"
  DESCENDING = "descending"


class QueryBase(BaseModel):
  page: int = Field(default=0)
  limit: int = Field(default=0)
  order: OrderSort = OrderSort.DESCENDING
  sort: str = Field(default='created_at')
