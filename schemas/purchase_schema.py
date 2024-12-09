from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from schemas.query_base import QueryBase
from models.purchase_model import Purchase
from models.purchase_detail_model import PurchaseDetail


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


class PurchaseListResponse(BaseModel):
  total: int = Field(...)
  items: list[Purchase] = Field(...)


class PurchaseWithDetail(BaseModel):
  purchase: Purchase = Field(...)
  detail: list[PurchaseDetail] = Field(...)
