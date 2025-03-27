from enum import Enum
from pydantic import Field

from models.entity import Entity


class PayWith(str, Enum):
  CASH = "CASH"
  DEBIT_CARD = "DEBIT_CARD"
  CREDIT_CARD = "CREDIT_CARD"
  TRANSFER = "TRANSFER"

  def return_description(self):
    _descriptions = {
        "CASH": "Efectivo",
        "DEBIT_CARD": "Tarjeta de débito",
        "CREDIT_CARD": "Tarjeta de crédito",
        "TRANSFER": "Transferencia"
    }
    return _descriptions[str(self.value)]


class Sale(Entity):
  total_amount: float = Field(...)
  pay_type: PayWith = Field(...)
  customer: str = Field(default='')
  user: str = Field(default='')

  def new(self, user: str):
    self.initialize()
    self.user = user

  def to_report(self) -> dict:
    sale_dict = self.model_dump(by_alias=True)
    sale_dict['_id'] = str(self.id)
    sale_dict['created_at'] = self.created_at.strftime("%d-%m-%Y %H:%M:%S")
    return sale_dict
