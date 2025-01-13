"""Routes y controllers de ventas"""
from datetime import datetime
import io
from fastapi import APIRouter, Depends, Query, status, Body
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import AuthService, OptionalHTTPBearer
from core import helpers_api, var_mongo_provider as mongo_provider
from models.sale_model import Sale
from services.sale_service import SaleService
from schemas.sale_schema import (
    SaleCreate, SaleQuery, SaleListResponse, SaleWithDetail, SaleQuery)
auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Sale"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/sales",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new sale"
)
async def sale_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme), sale: SaleCreate = Body(...)) -> Sale:
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  service = SaleService(mongo_provider.db)
  new_sale = service.create_sale(sale)
  return new_sale.model_dump(by_alias=True)

@router.get(
    "/sales/report",
    status_code=status.HTTP_200_OK,
    summary="Get purchases"
)
async def get_sales_report(query_params: SaleQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> StreamingResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = SaleService(mongo_provider.db)
  excel = service.download_report(query_params, with_detail=False)
  now = datetime.utcnow()
  filename = f'sales-report-{now.strftime("%Y%m%d%H%M")}.xlsx'

  response = StreamingResponse(
      io.BytesIO(excel),
      media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      headers={"Content-Disposition": f"attachment; filename={filename}"}
  )

  response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
  return response

@router.get(
    "/sales/report-detail",
    status_code=status.HTTP_200_OK,
    summary="Get purchases"
)
async def get_sales_report_detail(query_params: SaleQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> StreamingResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = SaleService(mongo_provider.db)
  excel = service.download_report(query_params, with_detail=True)
  now = datetime.utcnow()
  filename = f'sales-detail-report-{now.strftime("%Y%m%d%H%M")}.xlsx'

  response = StreamingResponse(
      io.BytesIO(excel),
      media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      headers={"Content-Disposition": f"attachment; filename={filename}"}
  )

  response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
  return response


@router.get(
    "/sales/{sale_id}",
    status_code=status.HTTP_200_OK,
    summary="Get sale by id"
)
async def sale_get_by_id(sale_id: str, token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> SaleWithDetail:
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  service = SaleService(mongo_provider.db)
  entity = service.get_sale_by_id(sale_id)
  sale = SaleWithDetail(**entity)
  return sale.model_dump(by_alias=True)


@router.get(
    "/sales",
    status_code=status.HTTP_200_OK,
    summary="Get sales"
)
async def get_sales(query_params: SaleQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> SaleListResponse:
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  service = SaleService(mongo_provider.db)
  query, pagination = service.get_query(query_params)
  sales = SaleListResponse(
      **helpers_api.get_paginator('sales', query, pagination))
  return sales.model_dump(by_alias=True)
