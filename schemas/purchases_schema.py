from pydantic import BaseModel, Field
from datetime import datetime
from schemas.query_base import QueryBase

class PurchasesResponse(BaseModel):
  id: str = Field(..., alias="_id")
  purchase_date: datetime = None
  supplier_id: str = Field(..., alias="supplier_id")
  total_amount: float = Field(...)
  created_at: datetime = None
  updated_at: datetime = None

class PurchasesCreateResponse(BaseModel):
  id: str = Field(..., alias="_id")
  purchase_date: datetime = None
  supplier_id: str = Field(..., alias="supplier_id")
  total_amount: float = Field(...)
  created_at: datetime = None
  updated_at: datetime = None

class PurchasesQuery(QueryBase):
  total_amount: float = Field(...)
  purchase_date: datetime = None

class SalesListResponse(BaseModel):
  total: int = Field(...)
  items: list[PurchasesCreateResponse] = Field(...)