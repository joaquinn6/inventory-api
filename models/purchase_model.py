from pydantic import BaseModel, Field

from models.entity import Entity


class Supplier(BaseModel):
  id: str = Field(..., alias="_id")
  code: str = Field(..., max_length=8)
  name: str = Field(...)


class Purchase(Entity):
  supplier: Supplier = Field(...)
  total_amount: float = Field(...)
  user: str = Field(default='')

  def new(self, user: str):
    self.initialize()
    self.user = user
    if isinstance(self.supplier, dict):
      self.supplier = Supplier(**self.supplier)

  def to_report(self) -> dict:
    purchase_dict = self.model_dump(by_alias=True)
    purchase_dict['_id'] = str(self.id)
    purchase_dict['created_at'] = self.created_at.strftime("%d-%m-%Y %H:%M:%S")
    purchase_dict['supplier.code'] = self.supplier.code
    purchase_dict['supplier.name'] = self.supplier.name
    return purchase_dict
