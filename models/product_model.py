from pydantic import BaseModel, Field
from datetime import datetime


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(...)
  description: str = Field(...)
  categories: list[str] = Field(...)
  purchase_price: float = Field(...)
  sale_price: float = Field(...)
  stock: int = Field(default=0)
  created_at: datetime = None
  updated_at: datetime = None
