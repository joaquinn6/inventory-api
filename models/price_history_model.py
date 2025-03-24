from enum import Enum
from datetime import datetime, timezone
from pydantic import Field

from models.entity import Entity


class PriceChangeType(str, Enum):
  SALE = "SALE"
  PURCHASE = "PURCHASE"


class PriceHistory(Entity):
  product_id: str = Field(...)
  type: PriceChangeType = PriceChangeType.PURCHASE
  price: float = Field(...)
  date: datetime | None = Field(default=None)

  def new(self):
    self.initialize()
    self.date = datetime.now(timezone.utc)
