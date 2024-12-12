from models.product_model import Product
from schemas.utils import divide_list
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from schemas.query_base import QueryBase
float


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
  purchase_price: float = Field(...)
  sale_price: float = Field(...)
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

  @field_validator("categories", mode="before")
  @classmethod
  def divide_categories(cls, value):
    return divide_list(value)


class ProductListResponse(BaseModel):
  total: int = Field(...)
  items: list[Product] = Field(...)
