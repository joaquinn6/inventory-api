"""Routes y controllers de productos"""
import io
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query, status, Body
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import AuthService, OptionalHTTPBearer
from core import helpers_api
from models.entity import PagedEntity
from models.product_model import Product
from repositories.product_repository import ProductRepository
from services.product_service import ProductService
from schemas.product_schema import ProductQuery

auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Products"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product"
)
async def product_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme), product: Product = Body(...)) -> Product:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = ProductService()
  new_product = service.create_product(product)
  return new_product.model_dump(by_alias=True)


@router.get(
    "/products/report",
    status_code=status.HTTP_200_OK,
    summary="Download products report"
)
async def get_products_report(query_params: ProductQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> StreamingResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = ProductService()
  excel = service.download_report(query_params)
  now = datetime.now(timezone.utc)
  filename = f'products-report-{now.strftime("%Y%m%d%H%M")}.xlsx'

  response = StreamingResponse(
      io.BytesIO(excel),
      media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      headers={"Content-Disposition": f"attachment; filename={filename}"}
  )

  response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
  return response


@router.get(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Get product by id"
)
async def product_get_by_id(product_id: str, token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Product:
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  repo = ProductRepository()
  entity = repo.get_by_id(product_id)
  if not entity:
    helpers_api.raise_error_404('Producto')
  service = ProductService()
  product_prices = service.get_prices_graph(entity.id)
  entity.graph = product_prices
  return entity.model_dump(by_alias=True)


@router.put(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Update product by id"
)
async def product_update_by_id(
        product_id: str,
        product: Product = Body(...),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Product:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  repo = ProductRepository()
  entity = repo.get_by_id(product_id)
  if not entity:
    helpers_api.raise_error_404('Producto')

  service = ProductService()
  update_product = service.update_product(entity, product)
  return update_product.model_dump(by_alias=True)


@router.get(
    "/products",
    status_code=status.HTTP_200_OK,
    summary="Get products"
)
async def get_products(query_params: ProductQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> PagedEntity:
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  service = ProductService()
  products = service.get_paged(query_params)
  return products.model_dump(by_alias=True)
