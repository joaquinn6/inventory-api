from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from models.sale_detail_model import SaleDetail
from models.sale_model import Sale, PayWith
from schemas.query_base import QueryBase
from schemas.utils import divide_format_query_dates, divide_list


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  units: int = Field(...)
  sale_price: float = Field(...)


class SaleCreate(BaseModel):
  products: list[Product] = Field(...)
  pay_type: PayWith = Field(...)
  customer: str = ''


class SaleQuery(QueryBase):
  date: tuple[datetime, datetime] = None
  code: str = None
  customer: str = ''
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
