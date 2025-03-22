from enum import Enum
from pydantic import Field

from models.entity import Entity


class PayWith(str, Enum):
  CASH = "CASH"
  DEBIT_CARD = "DEBIT_CARD"
  CREDIT_CARD = "CREDIT_CARD"
  TRANSFER = "TRANSFER"


class Sale(Entity):
  total_amount: float = Field(...)
  pay_type: PayWith = Field(...)
  customer: str = ''
