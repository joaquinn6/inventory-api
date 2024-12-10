from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from schemas.query_base import QueryBase
from schemas.utils import divide_list


class UserLogin(BaseModel):
  email: str = Field(...)
  password: str = Field(...)


class UserCreate(BaseModel):
  email: str = Field(...)
  roles: list[str] = Field(...)
  full_name: str = Field(...)
  password: str = Field(...)


class UserChangePassword(BaseModel):
  email: str = Field(...)
  password: str = Field(...)
  oldPassword: str = Field(...)


class UserUpdate(BaseModel):
  email: str = Field(...)
  roles: list[str] = Field(...)
  full_name: str = Field(...)


class UserResponse(BaseModel):
  id: str = Field(..., alias="_id")
  email: str = Field(...)
  roles: list[str] = Field(...)
  full_name: str = Field(...)
  active: bool = Field(...)
  created_at: datetime = None
  updated_at: datetime = None


class UserQuery(QueryBase):
  full_name: str = None
  email: str = None
  roles: list[str] = None
  state: str = 'ALL'

  @field_validator("roles", mode="before")
  @classmethod
  def divide_roles(cls, value):
    return divide_list(value)


class UserListResponse(BaseModel):
  total: int = Field(...)
  items: list[UserResponse] = Field(...)
