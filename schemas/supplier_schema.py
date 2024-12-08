from pydantic import BaseModel, Field
from models.supplier_model import Supplier
from schemas.query_base import QueryBase


class SupplierQuery(QueryBase):
  name: str = None
  code: str = None
  contact_name: str = None
  contact_email: str = None
  contact_phone: str = None


class Contact(BaseModel):
  name: str = ''
  email: str = ''
  phone: str = ''


class SupplierCreate(BaseModel):
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  contact: Contact = Field(...)


class SupplierUpdate(BaseModel):
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  contact: Contact = Field(...)


class SupplierListResponse(BaseModel):
  total: int = Field(...)
  items: list[Supplier] = Field(...)
