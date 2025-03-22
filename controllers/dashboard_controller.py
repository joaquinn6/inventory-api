"""Routes y controllers de dashboard"""
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from core import helpers_api
from core.auth import AuthService, OptionalHTTPBearer
from services.dashboard_service import DashboardService
auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Dashboard"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/dashboard",
    status_code=status.HTTP_200_OK,
    summary="Get dashboard"
)
async def get_sales(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> dict:
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  service = DashboardService()
  data = service.get_dashboard()
  return data
