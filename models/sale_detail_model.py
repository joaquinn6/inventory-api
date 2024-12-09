from pydantic import BaseModel, Field
from datetime import datetime


class SaleDetail(BaseModel):
  id: str = Field(..., alias="_id")
  sale_id: str = Field(...)
  product_id: str = Field(...)
  units: int = Field(...)
  unity_price: int = Field(...)
  created_at: datetime = None
  updated_at: datetime = None
