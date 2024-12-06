"""Routes y controllers de compras"""
from fastapi import Depends, Query, status, APIRouter
from core.auth import AuthService
from core import helpers_api, var_mongo_provider as mongo_provider
from fastapi.security import HTTPAuthorizationCredentials
from services.sales_service import PurchaseService
from schemas.sales_schema import PurchasesResponse, PurchasesListResponse

router = APIRouter(
    prefix="",
    tags=["Compras"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/purchases",
    status_code=status.HTTP_200_OK,
    summary="Get purchases by id"
)
async def get_purchases(query_params: PurchasesResponse = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> ProductListResponse:
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  service = PurchaseService(mongo_provider.db)
  query, pagination = service.get_query(query_params)
  purchases = PurchasesListResponse(
      **helpers_api.get_paginator('purchases', query, pagination))
  return purchases.model_dump(by_alias=True)