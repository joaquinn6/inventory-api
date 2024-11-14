"""Routes y controllers de usuarios"""
from fastapi import APIRouter, Depends, Query, status, Body
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import AuthService, OptionalHTTPBearer
from core import helpers_api, var_mongo_provider as mongo_provider
from models.product_model import Product
from services.product_service import ProductService
from schemas.product_schema import ProductCreate, ProductUpdate, ProductCreateResponse, ProductUpdateResponse, ProductQuery, ProductListResponse
auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Productos"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product"
)
async def product_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme), product: ProductCreate = Body(...)) -> ProductCreateResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = ProductService(mongo_provider.db)
  new_product = service.create_product(product)
  return new_product.model_dump(by_alias=True)


@router.get(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Get product by id"
)
async def product_get_by_id(product_id: str, token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Product:
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  entity = mongo_provider.db.products.find_one({'_id': product_id})
  if not entity:
    helpers_api.raise_error_404('Product')
  product = Product(**entity)
  return product.model_dump(by_alias=True)


@router.put(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Get product by id"
)
async def product_update_by_id(
        product_id: str,
        product: ProductUpdate = Body(...),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> ProductUpdateResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  entity = mongo_provider.db.products.find_one({'_id': product_id})
  if not entity:
    helpers_api.raise_error_404('Product')
  service = ProductService(mongo_provider.db)
  update_product = service.update_product(product_id, product)
  return update_product.model_dump(by_alias=True)


@router.get(
    "/products",
    status_code=status.HTTP_200_OK,
    summary="Get product by id"
)
async def get_products(query_params: ProductQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> ProductListResponse:
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  service = ProductService(mongo_provider.db)
  query, pagination = service.get_query(query_params)
  products = ProductListResponse(
      **helpers_api.get_paginator('products', query, pagination))
  return products.model_dump(by_alias=True)
