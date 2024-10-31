from pydantic import BaseModel, Field
from datetime import datetime


class UserLogin(BaseModel):
  email: str = Field(...)
  password: str = Field(...)


class UserCreate(BaseModel):
  email: str = Field(...)
  roles: list[str] = Field(...)
  full_name: str = Field(...)
  password: str = Field(...)


class UserResponse(BaseModel):
  id: str = Field(..., alias="_id")
  email: str = Field(...)
  roles: list[str] = Field(...)
  full_name: str = Field(...)
  created_at: datetime = None
  updated_at: datetime = None
