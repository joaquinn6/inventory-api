from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from decimal import Decimal


class PayWith(str, Enum):
  CASH = "CASH"
  DEBIT_CARD = "DEBIT_CARD"
  CREDIT_CARD = "CREDIT_CARD"
  TRANSFER = "TRANSFER"


class Sale(BaseModel):
  id: str = Field(..., alias="_id")
  total_amount: Decimal = Field(..., decimal_places=2)
  pay_type: PayWith = Field(...)
  customer: str = Field(...)
  created_at: datetime = None
  updated_at: datetime = None
