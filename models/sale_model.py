from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class PayWith(str, Enum):
  CASH = "CASH"
  DEBIT_CARD = "DEBIT_CARD"
  CREDIT_CARD = "CREDIT_CARD"
  TRANSFER = "TRANSFER"


class Sale(BaseModel):
  id: str = Field(..., alias="_id")
  total_amount: float = Field(...)
  pay_type: PayWith = Field(...)
  customer: str = Field(...)
  created_at: datetime = None
  updated_at: datetime = None
