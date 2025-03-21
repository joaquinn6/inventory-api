from enum import Enum
from typing import List
from pydantic import Field

from models.entity import Entity


class TrendTypes(str, Enum):
  UPWARD = "UPWARD"
  FALLING = "FALLING"
  EQUAL = "EQUAL"


class Product(Entity):
  name: str = Field(...)
  code: str = Field(...)
  description: str = Field(default='')
  categories: list[str] = Field(default=[])
  purchase_price: float = Field(default=0)
  sale_price: float = Field(default=0)
  stock: int = Field(default=0)
  trend: TrendTypes = TrendTypes.EQUAL
  graph: List[dict] = Field(default=[])

  def new(self):
    self.code = self.code.upper()
    self.description = self.description.capitalize()
    self.initialize()

  def update(self, new_item: "Product"):
    self.on_update()
    self.code = new_item.code.upper()
    self.name = new_item.name
    self.description = new_item.description.capitalize()
    self.categories = new_item.categories

  def to_report(self):
    product_dict = self.model_dump(by_alias=True)
    product_dict['categories'] = ", ".join(self.categories)
    product_dict['created_at'] = self.created_at.strftime("%d-%m-%Y %H:%M:%S")
    return product_dict
