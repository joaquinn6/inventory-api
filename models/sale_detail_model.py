from pydantic import BaseModel, Field

from models.entity import Entity


class Product(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(..., max_length=8)


class SaleDetail(Entity):
  sale_id: str = Field(...)
  product: Product = Field(...)
  units: int = Field(...)
  unity_price: float = Field(...)
  total_price: float = Field(...)
