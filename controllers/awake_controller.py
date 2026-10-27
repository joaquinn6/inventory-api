"""Routes y controllers para despertar la API"""
from fastapi import APIRouter, status
from core import var_mongo_provider as mongo_provider

router = APIRouter(
    prefix="",
    tags=["Awake"],
)


@router.get(
    "/awake",
    status_code=status.HTTP_200_OK,
    summary="Wake up the API and check the database connection"
)
async def awake() -> dict:
  mongo_provider.db.command('ping')
  return {'status': 'ok'}
