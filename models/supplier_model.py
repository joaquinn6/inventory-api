from pydantic import BaseModel, Field

from models.entity import Entity


class Contact(BaseModel):
  name: str = Field(default='')
  email: str = Field(default='')
  phone: str = Field(default='')


class Supplier(Entity):
  code: str = Field(..., max_length=8)
  name: str = Field(...)
  contact: Contact = Field(...)

  def new(self):
    self.code = self.code.upper()
    self.name = self.name.capitalize()
    self.contact.name = self.contact.name.title()
    self.initialize()

  def update(self, new_item: "Supplier"):
    self.on_update()
    self.code = new_item.code.upper()
    self.name = new_item.name.capitalize()
    self.contact = new_item.contact

  def to_report(self):
    supplier_dict = self.model_dump(by_alias=True)
    supplier_dict['contact.email'] = self.contact.email
    supplier_dict['contact.phone'] = self.contact.phone
    supplier_dict['contact.name'] = self.contact.name
    supplier_dict['created_at'] = self.created_at.strftime("%d-%m-%Y %H:%M:%S")
    return supplier_dict
