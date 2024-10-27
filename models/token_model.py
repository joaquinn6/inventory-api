from pydantic import BaseModel, Field


class Token(BaseModel):
  token: str = Field(...)
  email: str = Field(...)
  roles: list[str] = Field(...)
