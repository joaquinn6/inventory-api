"""Routes y controllers de usuarios"""
from fastapi import APIRouter, Depends, status, Body
from fastapi.security import HTTPAuthorizationCredentials
from core import helpers_api, var_mongo_provider as mongo_provider
from core.auth import AuthService, OptionalHTTPBearer
from services.user_service import UserService
from models.token_model import Token
from schemas.user_schema import UserCreate, UserLogin, UserResponse, UserQuery, UserListResponse, UserUpdate
from models.user_model import UserInfo
from fastapi import Query

auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Usuario"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def user_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme), user: UserCreate = Body(...)) -> UserResponse:
  if not AuthService().is_admin(token):
    helpers_api.raise_no_authorized()
  service = UserService(mongo_provider.db)
  new_user = service.create_user(user)
  return new_user.model_dump(by_alias=True)

@router.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by id"
)
async def user_get_by_id(user_id: str) -> UserInfo:
  entity = mongo_provider.db.users.find_one({'_id': user_id})
  if not entity:
    helpers_api.raise_error_404('User')
  user = UserInfo(**entity);
  return user.model_dump(by_alias=True)

@router.put(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Put user by id"
)
async def user_update_by_id(
        user_id: str,
        user: UserUpdate = Body(...),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> UserUpdate:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  entity = mongo_provider.db.users.find_one({'_id': user_id})
  if not entity:
    helpers_api.raise_error_404('User')
  service = UserService(mongo_provider.db)
  update_user = service.update_user(user_id, user)
  return update_user.model_dump(by_alias=True)

@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    summary="Get all users"
)
async def get_users(query_params: UserQuery = Query(...)) -> UserListResponse:
  service = UserService(mongo_provider.db)
  query, pagination = service.get_query(query_params)
  products = UserListResponse(
      **helpers_api.get_paginator('users', query, pagination))
  return products.model_dump(by_alias=True)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(user: UserLogin = Body(...)) -> Token:
  token = AuthService().generate_token(user.email, user.password)
  return token
