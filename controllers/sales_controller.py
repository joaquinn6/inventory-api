"""Routes y controllers de ventas"""
from fastapi import Query, status, APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import OptionalHTTPBearer
from core import helpers_api, var_mongo_provider as mongo_provider
from services.sales_service import SaleService
from schemas.sales_schema import SalesListResponse, SalesQuery
from core.auth import AuthService, OptionalHTTPBearer

auth_scheme = OptionalHTTPBearer()
router = APIRouter(
    prefix="",
    tags=["Ventas"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/sales",
    status_code=status.HTTP_200_OK,
    summary="Get sales"
)
async def get_sales(query_params: SalesQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> SalesListResponse:
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  service = SaleService(mongo_provider.db)
  query, pagination = service.get_query(query_params)
  sales = SalesListResponse(
      **helpers_api.get_paginator('sales', query, pagination))
  return sales.model_dump(by_alias=True)