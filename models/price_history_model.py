from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class PriceChangeType(str, Enum):
  SALE = "SALE"
  PURCHASE = "PURCHASE"


class PriceHistory(BaseModel):
  id: str = None
  product_id: str = Field(...)
  type: PriceChangeType
  price: float = Field(...)
  date: datetime = Field(...)
  reason: str = Field(...)
  created_at: datetime = None
