from datetime import datetime
import re
from pydantic import BaseModel, Field, field_validator
from schemas.utils import divide_list
from schemas.query_base import QueryBase


class ProductCreate(BaseModel):
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  description: str = Field(...)
  categories: list[str] = Field(...)


class ProductUpdate(BaseModel):
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  description: str = Field(...)
  categories: list[str] = Field(...)


class ProductCreateResponse(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  description: str = Field(...)
  categories: list[str] = Field(...)
  purchase_price: float = Field(...)
  sale_price: float = Field(...)
  stock: int = Field(default=0)
  created_at: datetime = None
  updated_at: datetime = None


class ProductUpdateResponse(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  description: str = Field(...)
  categories: list[str] = Field(...)


class ProductQuery(QueryBase):
  name: str = None
  code: str = None
  categories: list[str] = None
  stock: str = 'ALL'

  @field_validator("categories", mode="before")
  @classmethod
  def divide_categories(cls, value):
    return divide_list(value)

  def get_query(self) -> dict:
    query = dict({})

    if self.name:
      query['name'] = re.compile(f'.*{self.name}.*', re.I)

    if self.code:
      query['code'] = re.compile(f'{self.code.upper()}.*', re.I)
    if self.categories:
      query['categories'] = {'$in': self.categories}
    if self.stock != 'ALL':
      if self.stock == 'NO_STOCK':
        query['stock'] = 0
      else:
        query['stock'] = {'$gt': 0}
    return query
