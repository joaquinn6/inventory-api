from pydantic import BaseModel, Field


class QueryBase(BaseModel):
  page: int = Field(default=0)
  limit: int = Field(default=0)
  order: str = Field(default='-1')
  sort: str = Field(default='created_at')
