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


class Config(Entity):
  company: str = Field(default=Company())
  categories: List[Categories] = Field(default=[])
  currency: Currency = Field(default=Currency())

  @field_validator("categories", mode="before")
  @classmethod
  def str_to_dict(cls, value):
    if isinstance(value, str):
      return {'label': value, 'value': value.replace(' ', '_').upper()}
    return value

  def new(self):
    self.initialize()

  def update(self, new_item: "Config"):
    self.on_update()
    self.company = new_item.company
    self.categories = new_item.categories
