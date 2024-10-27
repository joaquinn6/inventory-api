from pydantic import BaseModel, Field


class User(BaseModel):
  id: str = None
  email: str = Field(...)
  roles: list[str] = Field(...)


class UserBase(User):
  email: str = Field(...)
  password: str = Field(...)
  full_name: str = Field(...)
  roles: list[str] = Field(...)


class UserLogin(BaseModel):
  email: str = Field(...)
  password: str = Field(...)
