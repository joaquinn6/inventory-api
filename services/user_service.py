from datetime import datetime
import shortuuid
import re
from core import helpers_api
from core.auth import AuthService
from schemas.user_schema import UserResponse, UserCreate, UserQuery, UserUpdate, deleteUser


class UserService():
  def __init__(self, database) -> None:
    self._database = database

  def create_user(self, user: UserCreate) -> UserResponse:
    exist_user = self._database.users.find_one({'email': user.email})
    if exist_user:
      helpers_api.raise_error_409('Email')

    entity = self._create_entity(user=user)
    entity['created_at'] = datetime.utcnow()
    entity['updated_at'] = datetime.utcnow()
    self._database.users.insert_one(entity)
    return UserResponse(**entity)

  def _create_entity(self, user: UserCreate) -> dict:
    return {
        '_id': shortuuid.uuid(),
        'email': user.email.lower(),
        'password': AuthService().get_password_hash(user.password),
        'roles': user.roles,
        'full_name': user.full_name
    }
  def get_query(self, query_params: UserQuery) -> tuple:
    pagination = self._get_pagination(query_params)
    query = self._get_query(query_params)
    query['active'] = True
    return query, pagination
  
  def _get_query(self, query_params: UserQuery) -> dict:
    query = dict({})
    if query_params.email:
      query['email'] = re.compile(f'.*{query_params.email}.*', re.I)
    return query
  
  def update_user(self, id_user: str, user: create_user) -> UserUpdate:
    exist_user = self._database.users.find_one({'_id': id_user})
    if not exist_user:
      helpers_api.raise_error_409('Code')

    entity = self._update_entity(user=user)
    entity['updated_at'] = datetime.utcnow()
    self._database.users.update_one({'_id': id_user}, {'$set': entity})
    entity['_id'] = id_user
    return UserUpdate(**entity)
  
  def delete_user(self, id_user: str) -> deleteUser:
    exist_user = self._database.users.find_one({'_id': id_user})
    if not exist_user:
      helpers_api.raise_error_409('Code')

    self._database.users.update_one({'_id': id_user}, {'$set': {'active': False}})
    entity = {
        'id': id_user,
        'active': False,
    }
    return deleteUser(**entity)
  
  def _update_entity(self, user: UserCreate) -> dict:
    return {
        'email': user.email,
        'full_name': user.full_name,
        'roles': user.roles,
    }

  def _get_pagination(self, query_params: UserQuery) -> dict:
    return {
        'page': query_params.page,
        'limit': query_params.limit,
        'order': query_params.order,
        'sort': query_params.sort
    }
