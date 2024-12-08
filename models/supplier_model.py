from pydantic import BaseModel, Field
from datetime import datetime


class Contact(BaseModel):
  name: str = ''
  email: str = ''
  phone: str = ''


class Supplier(BaseModel):
  id: str = Field(..., alias="_id")
  code: str = Field(..., max_length=8)
  name: str = Field(...)
  contact: Contact = Field(...)
  created_at: datetime = None
  updated_at: datetime = None
