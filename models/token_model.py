from pydantic import BaseModel, Field


class Token(BaseModel):
  id: str = Field(..., alias="_id")
  token: str = Field(...)
  email: str = Field(...)
  roles: list[str] = Field(...)
