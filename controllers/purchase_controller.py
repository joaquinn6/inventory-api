"""Routes y controllers de usuarios"""
from fastapi import APIRouter, Depends, Query, status, Body
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import AuthService, OptionalHTTPBearer
from core import helpers_api, var_mongo_provider as mongo_provider
from models.purchase_model import Purchase
from services.purchase_service import PurchaseService
from schemas.purchase_schema import (
    PurchaseCreate, PurchaseQuery, PurchaseListResponse, PurchaseWithDetail)
auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Purchase"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/purchases",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new purchase"
)
async def purchase_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme), purchase: PurchaseCreate = Body(...)) -> Purchase:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = PurchaseService(mongo_provider.db)
  new_purchase = service.create_purchase(purchase)
  return new_purchase.model_dump(by_alias=True)


@router.get(
    "/purchases/{purchase_id}",
    status_code=status.HTTP_200_OK,
    summary="Get purchase by id"
)
async def purchase_get_by_id(purchase_id: str, token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> PurchaseWithDetail:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = PurchaseService(mongo_provider.db)
  entity = service.get_purchase_by_id(purchase_id)
  purchase = PurchaseWithDetail(**entity)
  return purchase.model_dump(by_alias=True)


@router.get(
    "/purchases",
    status_code=status.HTTP_200_OK,
    summary="Get purchases"
)
async def get_purchases(query_params: PurchaseQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> PurchaseListResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = PurchaseService(mongo_provider.db)
  query, pagination = service.get_query(query_params)
  purchases = PurchaseListResponse(
      **helpers_api.get_paginator('purchases', query, pagination))
  return purchases.model_dump(by_alias=True)
