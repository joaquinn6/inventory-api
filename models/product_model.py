from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  description: str = Field(...)
  categories: list[str] = Field(...)
  purchase_price: Decimal = Field(..., decimal_places=2)
  sale_price: Decimal = Field(..., decimal_places=2)
  stock: int = Field(default=0)
  created_at: datetime = None
  updated_at: datetime = None
