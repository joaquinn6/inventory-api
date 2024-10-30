"""Routes y controllers de usuarios"""
from fastapi import APIRouter, Depends, status, Body
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import AuthService, OptionalHTTPBearer
from core import var_mongo_provider as mongo_provider
from services.product_service import ProductService
from schemas.product_schema import ProductCreate, ProductCreateResponse

auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Productos"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product"
)
async def product_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme), product: ProductCreate = Body(...)) -> ProductCreateResponse:
  if not AuthService().is_manager(token):
    AuthService().raise_unauthorized()
  service = ProductService(mongo_provider.db)
  new_product = service.create_product(product)
  return new_product.model_dump()
