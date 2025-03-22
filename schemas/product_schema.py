import re
from typing import List
from pydantic import field_validator
from schemas.utils import divide_list
from schemas.query_base import QueryBase


class ProductQuery(QueryBase):
  name: str = None
  code: str = None
  categories: List[str] = None
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
