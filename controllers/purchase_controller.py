"""Routes y controllers de compras"""
from datetime import datetime, timezone
import io
from fastapi import APIRouter, Depends, Query, status, Body
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials

from core import helpers_api
from core.auth import AuthService, OptionalHTTPBearer
from models.entity import PagedEntity
from models.purchase_model import Purchase
from schemas.purchase_schema import PurchaseCreate, PurchaseQuery, PurchaseWithDetail
from services.purchase_service import PurchaseService
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
  service = PurchaseService()
  new_purchase = service.create_purchase(purchase)
  return new_purchase.model_dump(by_alias=True)


@router.get(
    "/purchases/report",
    status_code=status.HTTP_200_OK,
    summary="Get purchases"
)
async def get_purchases_report(query_params: PurchaseQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> StreamingResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = PurchaseService()
  excel = service.download_report(query_params, with_detail=False)
  now = datetime.now(timezone.utc)
  filename = f'purchases-report-{now.strftime("%Y%m%d%H%M")}.xlsx'

  response = StreamingResponse(
      io.BytesIO(excel),
      media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      headers={"Content-Disposition": f"attachment; filename={filename}"}
  )

  response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
  return response


@router.get(
    "/purchases/report-detail",
    status_code=status.HTTP_200_OK,
    summary="Get purchases"
)
async def get_purchases_report_detail(query_params: PurchaseQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> StreamingResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = PurchaseService()
  excel = service.download_report(query_params, with_detail=True)
  now = datetime.now(timezone.utc)
  filename = f'purchases-detail-report-{now.strftime("%Y%m%d%H%M")}.xlsx'

  response = StreamingResponse(
      io.BytesIO(excel),
      media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      headers={"Content-Disposition": f"attachment; filename={filename}"}
  )

  response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
  return response


@router.get(
    "/purchases/{purchase_id}",
    status_code=status.HTTP_200_OK,
    summary="Get purchase by id"
)
async def purchase_get_by_id(purchase_id: str, token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> PurchaseWithDetail:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = PurchaseService()
  entity = service.get_purchase_by_id(purchase_id)
  return entity.model_dump(by_alias=True)


@router.get(
    "/purchases",
    status_code=status.HTTP_200_OK,
    summary="Get purchases"
)
async def get_purchases(query_params: PurchaseQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> PagedEntity:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = PurchaseService()
  purchases = service.get_paged(query_params)
  return purchases.model_dump(by_alias=True)
