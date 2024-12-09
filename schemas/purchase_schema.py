from typing import Union, Tuple
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from schemas.query_base import QueryBase
from models.purchase_model import Purchase
from models.purchase_detail_model import PurchaseDetail
from schemas.utils import parse_amount_query


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  units: str = Field(...)
  unit_purchase_price: float = Field(...)
  unit_sale_price: float = Field(...)


class PurchaseCreate(BaseModel):
  supplier_id: str = Field(...)
  products: list[Product] = Field(..., max_length=8)


class PurchaseQuery(QueryBase):
  date: tuple[datetime, datetime] = None
  supplier: str = None
  amount: Union[Tuple[int, str], Tuple[int, int]] = Field(default=(0, "MAX"))

  @field_validator("amount", mode="before")
  @classmethod
  def validate_item(cls, value):
    return parse_amount_query(value)


class PurchaseListResponse(BaseModel):
  total: int = Field(...)
  items: list[Purchase] = Field(...)


class PurchaseWithDetail(BaseModel):
  purchase: Purchase = Field(...)
  detail: list[PurchaseDetail] = Field(...)
