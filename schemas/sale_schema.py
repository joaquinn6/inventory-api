from datetime import datetime
import re
from typing import List
from pydantic import BaseModel, Field, field_validator
import pytz
from models.sale_detail_model import SaleDetail
from models.sale_model import Sale, PayWith
from schemas.query_base import QueryBase
from schemas.utils import divide_format_query_dates, divide_list


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  units: int = Field(...)
  sale_price: float = Field(...)


class SaleCreate(BaseModel):
  products: List[Product] = Field(...)
  pay_type: PayWith = Field(...)
  customer: str = ''


class SaleQuery(QueryBase):
  date: tuple[datetime, datetime] = None
  code: str = None
  customer: str = ''
  pay_types: List[PayWith] = None
  amount: List[int] = [0, 5000]

  @field_validator("date", mode="before")
  @classmethod
  def divide_dates(cls, value):
    try:
      if value is None:
        return None
      if isinstance(value, tuple) and len(value) == 2:
        return value
      return divide_format_query_dates(value)
    except ValueError:
      return None

  @field_validator("amount", mode="before")
  @classmethod
  def divide_amount(cls, value):
    return divide_list(value)

  def get_query(self) -> dict:
    query = dict({})

    if self.date is not None:
      query['created_at'] = {
          '$gte': self.date[0].astimezone(pytz.utc),
          '$lte':  self.date[1].astimezone(pytz.utc)
      }

    if self.code:
      query['_id'] = self.code

    if self.customer:
      query['customer'] = re.compile(f'.*{self.customer}.*', re.I)

    if self.pay_types:
      query['pay_type'] = {'$in': self.pay_types}

    if self.amount:
      if self.amount[1] != 5000:
        query['total_amount'] = {
            '$gte': self.amount[0], '$lte':  self.amount[1]}
      else:
        query['total_amount'] = {'$gte': self.amount[0]}
    return query


class SaleWithDetail(BaseModel):
  sale: Sale = Field(...)
  detail: List[SaleDetail] = Field(...)
