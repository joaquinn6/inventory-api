"""Routes y controllers de usuarios"""
from datetime import datetime
from io import BytesIO
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import AuthService, OptionalHTTPBearer
from core import helpers_api, var_mongo_provider as mongo_provider
from services.config_service import ConfigService
auth_scheme = OptionalHTTPBearer()

router = APIRouter(
    prefix="",
    tags=["Config"],
    responses={404: {"description": "Not found"}},
)


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
  now = datetime.utcnow()
  filename = f'backup-{now.strftime("%Y%m%d%H%M")}.zip'
  return StreamingResponse(
      backup_file,
      media_type="application/zip",
      headers={"Content-Disposition": f"attachment; filename={filename}"}
  )


@router.post(
    "/config/restore",
    status_code=status.HTTP_200_OK,
    summary="Create a backup of the database"
)
async def restore_post(token: HTTPAuthorizationCredentials = Depends(auth_scheme), file: UploadFile = File(...)) -> StreamingResponse:
  if not AuthService().is_manager(token):
    helpers_api.raise_no_authorized()

  zip_file = BytesIO(await file.read())
  service = ConfigService(mongo_provider.db)
  result = service.restore_db(zip_file)
  return result
