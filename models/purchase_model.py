from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class Supplier(BaseModel):
  id: str = Field(..., alias="_id")
  code: str = Field(..., max_length=8)
  name: str = Field(...)


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(..., max_length=8)


class Purchase(BaseModel):
  id: str = Field(..., alias="_id")
  supplier: Supplier = Field(...)
  total_amount: Decimal = Field(..., decimal_places=2)
  created_at: datetime = None
