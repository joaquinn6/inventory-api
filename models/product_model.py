from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TrendTypes(str, Enum):
  UPWARD = "UPWARD"
  FALLING = "FALLING"
  EQUAL = "EQUAL"


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  description: str = Field(...)
  categories: list[str] = Field(...)
  purchase_price: float = Field(...)
  sale_price: float = Field(...)
  stock: int = Field(default=0)
  trend: TrendTypes = TrendTypes.EQUAL
  created_at: datetime = None
  updated_at: datetime = None
