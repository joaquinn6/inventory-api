from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from schemas.query_base import QueryBase
from models.sale_model import Sale, PayWith
from models.sale_detail_model import SaleDetail
from schemas.utils import divide_format_query_dates, divide_list


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  units: str = Field(...)
  price: Decimal = Field(..., decimal_places=2)


class SaleCreate(BaseModel):
  products: list[Product] = Field(..., max_length=8)
  pay_type: PayWith = Field(...)
  customer: str = Field(...)


class SaleQuery(QueryBase):
  date: tuple[datetime, datetime] = None
  customer: str = None
  pay_types: list[PayWith] = None
  amount: list[int] = [0, 5000]

  @field_validator("date", mode="before")
  @classmethod
  def divide_dates(cls, value):
    return divide_format_query_dates(value)

  @field_validator("amount", mode="before")
  @classmethod
  def divide_amount(cls, value):
    return divide_list(value)


class SaleListResponse(BaseModel):
  total: int = Field(...)
  items: list[Sale] = Field(...)


class SaleWithDetail(BaseModel):
  sale: Sale = Field(...)
  detail: list[SaleDetail] = Field(...)
