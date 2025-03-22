from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator
import pytz
from schemas.utils import divide_list, divide_format_query_dates
from schemas.query_base import QueryBase
from models.purchase_detail_model import PurchaseDetail
from models.purchase_model import Purchase


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  units: int = Field(...)
  purchase_price: float = Field(...)
  sale_price: float = Field(...)


class PurchaseCreate(BaseModel):
  supplier_id: str = Field(...)
  products: List[Product] = Field(...)


class PurchaseQuery(QueryBase):
  date: tuple[datetime, datetime] = None
  code: str = None
  supplier: str = None
  amount: list[int] = [0, 10000]

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
          '$lte': self.date[1].astimezone(pytz.utc)
      }

    if self.code:
      query['_id'] = self.code

    if self.supplier:
      query['supplier._id'] = self.supplier

    if self.amount:
      if self.amount[1] != 10000:
        query['total_amount'] = {
            '$gte': self.amount[0], '$lte':  self.amount[1]}
      else:
        query['total_amount'] = {'$gte': self.amount[0]}
    return query


class PurchaseWithDetail(BaseModel):
  purchase: Purchase = Field(...)
  detail: List[PurchaseDetail] = Field(...)
