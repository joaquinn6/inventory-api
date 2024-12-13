from pydantic import BaseModel, Field
from datetime import datetime


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(..., max_length=8)


class PurchaseDetail(BaseModel):
  id: str = Field(..., alias="_id")
  purchase_id: str = Field(...)
  product: Product = Field(...)
  units: int = Field(...)
  unity_price: float = Field(...)
  total_price: float = Field(...)
  created_at: datetime = None
