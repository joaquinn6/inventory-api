from pydantic import BaseModel, Field
from datetime import datetime


class Contact(BaseModel):
  name: str = Field(...)
  email: str = ''
  phone: str = ''


class Supplier(BaseModel):
  id: str = None
  name: str = Field(...)
  contact: Contact = Field(...)
  created_at: datetime = None
  updated_at: datetime = None
