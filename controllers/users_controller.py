"""Routes y controllers de usuarios"""
from fastapi import APIRouter, Depends, status, Body
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import AuthService, OptionalHTTPBearer
from core import var_mongo_provider as mongo_provider
from services.user_service import UserService
from models.token_model import Token
from schemas.user_schema import UserCreate, UserLogin, UserResponse

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
    AuthService().raise_unauthorized()
  service = UserService(mongo_provider.db)
  new_user = service.create_user(user)
  return new_user.model_dump()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(user: UserLogin = Body(...)) -> Token:
  token = AuthService().generate_token(user.email, user.password)
  return token
