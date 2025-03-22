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

  def new(self):
    self.initialize()

  def to_report(self) -> dict:
    sale_dict = self.model_dump(by_alias=True)
    sale_dict['_id'] = str(self.id)
    sale_dict['created_at'] = self.created_at.strftime("%d-%m-%Y %H:%M:%S")
    return sale_dict
