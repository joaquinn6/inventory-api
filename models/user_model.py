from pydantic import BaseModel, Field
from datetime import datetime


class User(BaseModel):
  id: str = None
  email: str = Field(...)
  roles: list[str] = Field(...)
  full_name: str = Field(...)
  password: str = Field(...)
  created_at: datetime = None
  updated_at: datetime = None
