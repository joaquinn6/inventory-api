from pydantic import BaseModel, Field
from datetime import datetime
from schemas.query_base import QueryBase
from models.sale_model import Sale, PayWith
from models.sale_detail_model import SaleDetail


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  units: str = Field(...)
  price: float = Field(...)


class SaleCreate(BaseModel):
  products: list[Product] = Field(..., max_length=8)
  pay_type: PayWith = Field(...)
  customer: str = Field(...)


class SaleQuery(QueryBase):
  date: tuple[datetime, datetime] = None
  customer: str = None
  pay_types: list[PayWith] = None
  amount: tuple[int, int | str] = tuple([0, 'MAX'])


class SaleListResponse(BaseModel):
  total: int = Field(...)
  items: list[Sale] = Field(...)


class SaleWithDetail(BaseModel):
  sale: Sale = Field(...)
  detail: list[SaleDetail] = Field(...)
