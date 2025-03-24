"""Routes y controllers de configuración"""
from datetime import datetime, timezone
from io import BytesIO
from fastapi import APIRouter, Body, Depends, status, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import AuthService, OptionalHTTPBearer
from core import helpers_api, var_mongo_provider as mongo_provider
from models.config_model import Config
from repositories.config import ConfigRepository
from services.config_service import ConfigService
auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Config"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/config",
    status_code=status.HTTP_200_OK,
    summary="Get config"
)
async def get_config(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Config:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  repo = ConfigRepository()
  entity = repo.get_one({})
  if not entity:
    return Config().model_dump(by_alias=True)
  return entity.model_dump(by_alias=True)


@router.put(
    "/config",
    status_code=status.HTTP_200_OK,
    summary="Update config"
)
async def config_update(
        config: Config = Body(...),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Config:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  repo = ConfigRepository()
  entity = repo.get_one({})
  if not entity:
    helpers_api.raise_error_404('Configuración')

  service = ConfigService(mongo_provider.db)
  update_config = service.update_config(entity, config)
  return update_config.model_dump(by_alias=True)


@router.post(
    "/config",
    status_code=status.HTTP_200_OK,
    summary="Create config"
)
async def config_create(
        config: Config = Body(...),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Config:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()

  service = ConfigService(mongo_provider.db)
  service.create_config(config)
  return config.model_dump(by_alias=True)


@router.post(
    "/config/backup",
    status_code=status.HTTP_200_OK,
    summary="Create a backup of the database"
)
async def backup_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> StreamingResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()
  service = ConfigService(mongo_provider.db)
  backup_file = service.create_backup()
  now = datetime.now(timezone.utc)
  filename = f'backup-{now.strftime("%Y%m%d%H%M")}.zip'

  response = StreamingResponse(
      backup_file,
      media_type="application/zip",
      headers={"Content-Disposition": f"attachment; filename={filename}"}
  )

  response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
  return response


@router.post(
    "/config/restore",
    status_code=status.HTTP_200_OK,
    summary="Create a backup of the database"
)
async def restore_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme), file: UploadFile = File(...)):
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()

  zip_file = BytesIO(await file.read())
  service = ConfigService(mongo_provider.db)
  service.restore_db(zip_file)
  return
