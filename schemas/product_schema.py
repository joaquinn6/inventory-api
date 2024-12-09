from datetime import datetime
from pydantic import BaseModel, Field
from schemas.query_base import QueryBase
from decimal import Decimal


class ProductCreate(BaseModel):
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  description: str = Field(...)
  categories: list[str] = Field(...)


class ProductUpdate(BaseModel):
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  description: str = Field(...)
  categories: list[str] = Field(...)


class ProductCreateResponse(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  description: str = Field(...)
  categories: list[str] = Field(...)
  purchase_price: Decimal = Field(..., decimal_places=2)
  sale_price: Decimal = Field(..., decimal_places=2)
  stock: int = Field(default=0)
  created_at: datetime = None
  updated_at: datetime = None


class ProductUpdateResponse(BaseModel):
  id: str = Field(..., alias="_id")
  name: str = Field(...)
  code: str = Field(..., max_length=8)
  description: str = Field(...)
  categories: list[str] = Field(...)


class ProductQuery(QueryBase):
  name: str = None
  code: str = None
  categories: list[str] = None
  stock: str = 'ALL'


class ProductListResponse(BaseModel):
  total: int = Field(...)
  items: list[ProductCreateResponse] = Field(...)
