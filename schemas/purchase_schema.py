from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from models.purchase_model import Purchase
from models.purchase_detail_model import PurchaseDetail
from schemas.query_base import QueryBase
from schemas.utils import divide_list, divide_format_query_dates


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  units: str = Field(...)
  unit_purchase_price: Decimal = Field(..., decimal_places=2)
  unit_sale_price: Decimal = Field(..., decimal_places=2)


class PurchaseCreate(BaseModel):
  supplier_id: str = Field(...)
  products: list[Product] = Field(..., max_length=8)


class PurchaseQuery(QueryBase):
  date: tuple[datetime, datetime] = None
  supplier: str = None
  amount: list[int] = [0, 10000]

  @field_validator("date", mode="before")
  @classmethod
  def divide_dates(cls, value):
    return divide_format_query_dates(value)

  @field_validator("amount", mode="before")
  @classmethod
  def divide_amount(cls, value):
    return divide_list(value)


class PurchaseListResponse(BaseModel):
  total: int = Field(...)
  items: list[Purchase] = Field(...)


class PurchaseWithDetail(BaseModel):
  purchase: Purchase = Field(...)
  detail: list[PurchaseDetail] = Field(...)
