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

  def new(self):
    self.initialize()
    if isinstance(self.product, dict):
      self.product = Product(**self.product)

  def to_report(self) -> dict:
    detail_dict = self.model_dump(by_alias=True)
    detail_dict['product.code'] = self.product.code
    detail_dict['product.name'] = self.product.name
    return detail_dict
