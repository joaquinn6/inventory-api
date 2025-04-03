from enum import Enum
from typing import List
from pydantic import BaseModel, Field, field_validator

from models.entity import Entity


class Company(BaseModel):
  name: str = Field(default='')
  slogan: str = Field(default='')
  address: str = Field(default='')
  phone: str = Field(default='')
  email: str = Field(default='')
  logo: str = Field(default='')


class Categories(BaseModel):
  label: str = Field(default='')
  value: str = Field(default='')


class Currencies(str, Enum):
  USD = "USD"
  EUR = "EUR"
  NIO = "NIO"


class Currency(BaseModel):
  value: str = Field(default=Currencies.NIO)
  symbol: str = Field(default='C$')


class ConfigProduct(BaseModel):
  auto_code: bool = Field(default=False)
  prefix_code: str = Field(default='')
  categories: List[Categories] = Field(default=[])

  @field_validator("categories", mode="before")
  @classmethod
  def str_to_dict(cls, values):
    for (index, value) in enumerate(values):
      if isinstance(value, str):
        values[index] = {
            'label': value.capitalize(),
            'value': value.replace(' ', '_').upper()
        }
    return values


class Config(Entity):
  company: Company = Field(default=Company())
  currency: Currency = Field(default=Currency())
  product: ConfigProduct = Field(default=ConfigProduct())

  def new(self):
    self.initialize()

  def update(self, new_item: "Config"):
    self.on_update()
    self.company = new_item.company
    self.currency = new_item.currency
    self.product = new_item.product
