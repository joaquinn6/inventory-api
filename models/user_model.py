from pydantic import BaseModel, Field
from datetime import datetime


class User(BaseModel):
  id: str = Field(..., alias="_id")
  email: str = Field(...)
  roles: list[str] = Field(...)
  full_name: str = Field(...)
  password: str = Field(...)
  active: bool = Field(...)
  created_at: datetime = None
  updated_at: datetime = None


class UserInfo(BaseModel):
  id: str = Field(..., alias="_id")
  email: str = Field(...)
  roles: list[str] = Field(...)
  full_name: str = Field(...)
  active: bool = Field(...)
  created_at: datetime = None
  updated_at: datetime = None
