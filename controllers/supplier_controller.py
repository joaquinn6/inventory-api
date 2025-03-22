"""Routes y controllers de proveedores"""
import io
from datetime import datetime
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, Query, status, Body
from fastapi.security import HTTPAuthorizationCredentials

from core import helpers_api
from core.auth import AuthService, OptionalHTTPBearer
from models.entity import PagedEntity
from models.supplier_model import Supplier
from repositories.supplier_repository import SupplierRepository
from services.supplier_service import SupplierService
from schemas.supplier_schema import SupplierQuery
auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Suppliers"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/suppliers",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new supplier"
)
async def supplier_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme), supplier: Supplier = Body(...)) -> Supplier:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = SupplierService()
  new_supplier = service.create_supplier(supplier)
  return new_supplier.model_dump(by_alias=True)


@router.get(
    "/suppliers/report",
    status_code=status.HTTP_200_OK,
    summary="Download suppliers report"
)
async def get_suppliers_report(query_params: SupplierQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> StreamingResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = SupplierService()
  excel = service.download_report(query_params)
  now = datetime.utcnow()
  filename = f'suppliers-{now.strftime("%Y%m%d%H%M")}.xlsx'

  response = StreamingResponse(
      io.BytesIO(excel),
      media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      headers={"Content-Disposition": f"attachment; filename={filename}"}
  )

  response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
  return response


@router.get(
    "/suppliers/{supplier_id}",
    status_code=status.HTTP_200_OK,
    summary="Get supplier by id"
)
async def supplier_get_by_id(supplier_id: str, token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Supplier:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  repo = SupplierRepository()
  entity = repo.get_by_id(supplier_id)
  if not entity:
    helpers_api.raise_error_404('Proveedor')
  return entity.model_dump(by_alias=True)


@router.put(
    "/suppliers/{supplier_id}",
    status_code=status.HTTP_200_OK,
    summary="Update supplier by id"
)
async def supplier_update_by_id(
        supplier_id: str,
        supplier: Supplier = Body(...),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Supplier:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  repo = SupplierRepository()
  entity = repo.get_by_id(supplier_id)
  if not entity:
    helpers_api.raise_error_404('Proveedor')

  service = SupplierService()
  update_supplier = service.update_supplier(entity, supplier)
  return update_supplier.model_dump(by_alias=True)


@router.get(
    "/suppliers",
    status_code=status.HTTP_200_OK,
    summary="Get suppliers"
)
async def get_suppliers(query_params: SupplierQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> PagedEntity:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = SupplierService()
  suppliers = service.get_paged(query_params)
  return suppliers.model_dump(by_alias=True)
