from pydantic import BaseModel, Field
from datetime import datetime
from schemas.query_base import QueryBase
from models.purchase_model import Purchase
from models.purchase_detail_model import PurchaseDetail


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
  products: list[str] = None
  amount: tuple[int, int | str] = tuple(0, 'MAX')


class PurchaseListResponse(BaseModel):
  total: int = Field(...)
  items: list[Purchase] = Field(...)


class PurchaseWithDetail(BaseModel):
  purchase: Purchase = Field(...)
  detail: list[PurchaseDetail] = Field(...)
