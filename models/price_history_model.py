from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal


class PriceChangeType(str, Enum):
  SALE = "SALE"
  PURCHASE = "PURCHASE"


class PriceHistory(BaseModel):
  id: str = Field(..., alias="_id")
  product_id: str = Field(...)
  type: PriceChangeType = PriceChangeType.PURCHASE
  price: Decimal = Field(..., decimal_places=2)
  date: datetime = Field(...)
  created_at: datetime = None
