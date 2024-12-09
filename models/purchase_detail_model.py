from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(..., max_length=8)


class PurchaseDetail(BaseModel):
  id: str = Field(..., alias="_id")
  purchase_id: str = Field(...)
  product: Product = Field(...)
  units: int = Field(...)
  unity_price: Decimal = Field(..., decimal_places=2)
  total_price: Decimal = Field(..., decimal_places=2)
  created_at: datetime = None
  updated_at: datetime = None
