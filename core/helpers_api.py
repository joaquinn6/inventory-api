import pymongo
from fastapi import HTTPException, status
from core import var_mongo_provider as mongo_provider
from schemas.query_base import OrderSort


def get_paginator(collection: str, query: dict, pagination: dict, fct=None, project=None) -> dict:
  page_size = 0
  page_num = 0
  sort = "created_at"
  sort_direction = pymongo.DESCENDING
  if "limit" in pagination:
    page_size = int(pagination['limit'])

  if "page" in pagination:
    page_num = int(pagination['page']) - 1

  if "sort" in pagination:
    sort = pagination['sort']

  if "order" in pagination:
    if pagination['order'] == OrderSort.ASCENDING:
      sort_direction = pymongo.ASCENDING
    elif pagination['order'] == OrderSort.DESCENDING:
      sort_direction = pymongo.DESCENDING

  coll = mongo_provider.db.get_collection(collection)
  total = coll.count_documents(query)
  ordenes = [(sort, sort_direction)]
  if sort != "created_at":
    ordenes.append(("_id", pymongo.DESCENDING))

  skips = 0
  if page_size != 0:
    skips = page_size * page_num

  cursor = None
  if page_size == 0:
    cursor = coll.find(query, project).sort(ordenes)
  else:
    cursor = coll.find(query, project).sort(
        ordenes).skip(skips).limit(page_size)

  entities = list([])
  for entity in cursor:
    if fct:
      fct(entity)
    entities.append(entity)

  return {'total': total, 'items': entities}


def raise_error_404(entity: str = 'Entity'):
  raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"{entity} not found",
      headers={"WWW-Authenticate": "Bearer"},
  )


def raise_error_400(message: str = 'Entity'):
  raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"{message}",
      headers={"WWW-Authenticate": "Bearer"},
  )


def raise_error_409(entity: str = 'Entity'):
  raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail=f"{entity} already  exist",
      headers={"WWW-Authenticate": "Bearer"},
  )


def raise_error_422(entity: str = 'Contraseña'):
  raise HTTPException(
      # Usando 422 Unprocessable Entity
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
      detail=f"{entity} actual es incorrecta.",
      headers={"WWW-Authenticate": "Bearer"},
  )


def raise_no_authorized():
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="You are not authorized for this action",
      headers={"WWW-Authenticate": "Bearer"},
  )
  raise credentials_exception
