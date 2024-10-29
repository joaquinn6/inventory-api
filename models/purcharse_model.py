from pydantic import BaseModel, Field
from datetime import datetime


class Purchase(BaseModel):
  id: str = None
  date: datetime = None
  supplier_id: str = Field(...)
  total_amount: float = Field(...)
  created_at: datetime = None
  updated_at: datetime = None
