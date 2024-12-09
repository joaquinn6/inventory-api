from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from schemas.query_base import QueryBase
from models.sale_model import Sale, PayWith
from models.sale_detail_model import SaleDetail


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
  amount: list[int] = [0, 10000]


class SaleListResponse(BaseModel):
  total: int = Field(...)
  items: list[Sale] = Field(...)


class SaleWithDetail(BaseModel):
  sale: Sale = Field(...)
  detail: list[SaleDetail] = Field(...)
