from pydantic import BaseModel, Field
from datetime import datetime
from schemas.query_base import QueryBase


class SalesResponse(BaseModel):
  id: str = Field(..., alias="_id")
  total_amount: float = Field(...)
  sale_date: datetime = None
  created_at: datetime = None
  updated_at: datetime = None


class SalesQuery(QueryBase):
  total_amount: float = None
  sale_date: datetime = None


class SalesListResponse(BaseModel):
  total: int = Field(...)
  items: list[SalesResponse] = Field(...)
