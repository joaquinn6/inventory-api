from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class PriceChangeType(str, Enum):
  SALE = "SALE"
  PURCHASE = "PURCHASE"


class PriceHistory(BaseModel):
  id: str = Field(..., alias="_id")
  product_id: str = Field(...)
  type: PriceChangeType = PriceChangeType.PURCHASE
  price: float = Field(...)
  date: datetime = Field(...)
  created_at: datetime = None
