from pydantic import BaseModel, Field
from datetime import datetime


class Sale(BaseModel):
  id: str = Field(..., alias="_id")
  date: str = Field(...)
  total_amount: float = Field(...)
  created_at: datetime = None
  updated_at: datetime = None
