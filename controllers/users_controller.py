"""Routes y controllers de usuarios"""
from datetime import datetime, timezone
import io
from fastapi import Query
from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials

from core import helpers_api
from core.auth import AuthService, OptionalHTTPBearer
from repositories.user_repository import UserRepository
from services.user_service import UserService
from models.entity import PagedEntity
from models.token_model import Token
from models.user_model import User, UserInfo
from schemas.user_schema import UserLogin, UserQuery, UserChangePassword

auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Usuario"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/users/{user_id}/password",
    status_code=status.HTTP_200_OK,
    summary="Change password"
)
async def change_password(user_id: str, token: HTTPAuthorizationCredentials = Depends(auth_scheme), body: UserChangePassword = Body(...)):
  if not AuthService().is_sales(token):
    helpers_api.raise_no_authorized()
  repo = UserRepository()
  entity = repo.get_by_id(user_id)
  if not entity:
    helpers_api.raise_error_404('Usuario')

  service = UserService()
  service.change_password(body, entity)
  return


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def user_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme), user: User = Body(...)) -> UserInfo:
  if not AuthService().is_admin(token):
    helpers_api.raise_no_authorized()
  service = UserService()
  new_user = service.create_user(user)
  return new_user.model_dump(by_alias=True)


@router.get(
    "/users/report",
    status_code=status.HTTP_200_OK,
    summary="Download users report"
)
async def get_users_report(query_params: UserQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> StreamingResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = UserService()
  excel = service.download_report(query_params)
  now = datetime.now(timezone.utc)
  filename = f'users-report-{now.strftime("%Y%m%d%H%M")}.xlsx'

  response = StreamingResponse(
      io.BytesIO(excel),
      media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      headers={"Content-Disposition": f"attachment; filename={filename}"}
  )

  response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
  return response


@router.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by id"
)
async def user_get_by_id(user_id: str, token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> UserInfo:
  if not AuthService().is_admin(token):
    helpers_api.raise_no_authorized()
  repo = UserRepository()
  entity = repo.get_by_id(user_id)
  if not entity:
    helpers_api.raise_error_404('Usuario')
  return UserInfo.from_dict(entity.model_dump(by_alias=True)).model_dump(by_alias=True)


@router.put(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Update user by id"
)
async def user_update_by_id(
        user_id: str,
        user: User = Body(...),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> UserInfo:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  repo = UserRepository()
  entity = repo.get_by_id(user_id)
  if not entity:
    helpers_api.raise_error_404('Proveedor')

  service = UserService()
  update_user = service.update_user(entity, user)
  return update_user.model_dump(by_alias=True)


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    summary="Get users"
)
async def get_users(query_params: UserQuery = Query(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> PagedEntity:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = UserService()
  suppliers = service.get_paged(query_params)
  return suppliers.model_dump(by_alias=True)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(user: UserLogin = Body(...)) -> Token:
  token = AuthService().generate_token(user.email, user.password)
  return token


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Desactive user by id"
)
async def user_delete_by_id(
        user_id: str,
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> UserInfo:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  repo = UserRepository()
  entity = repo.get_by_id(user_id)
  if not entity:
    helpers_api.raise_error_404('Usuario')
  service = UserService()
  delete_user = service.delete_user(entity)
  return delete_user.model_dump(by_alias=True)


@router.put(
    "/users/{user_id}/active",
    status_code=status.HTTP_200_OK,
    summary="Active user by id"
)
async def user_active_by_id(
        user_id: str,
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> UserInfo:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  repo = UserRepository()
  entity = repo.get_by_id(user_id)
  if not entity:
    helpers_api.raise_error_404('Usuario')
  service = UserService()
  active_user = service.active_user(entity)
  return active_user.model_dump(by_alias=True)
