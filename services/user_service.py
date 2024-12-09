from datetime import datetime
import re
import shortuuid
from core import helpers_api
from core.auth import AuthService
from schemas.user_schema import UserResponse, UserCreate, UserQuery, UserUpdate, UserChangePassword


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
        'full_name': user.full_name,
        'active': True
    }

  def get_query(self, query_params: UserQuery) -> tuple:
    pagination = self._get_pagination(query_params)
    query = self._get_query(query_params)
    return query, pagination

  def _get_query(self, query_params: UserQuery) -> dict:
    query = dict({})
    if query_params.email:
      query['email'] = re.compile(f'.*{query_params.email}.*', re.I)

    if query_params.full_name:
      query['full_name'] = re.compile(f'.*{query_params.full_name}.*', re.I)

    if query_params.roles:
      query['roles'] = {'$in': query_params.roles}

    if query_params.state != 'ALL':
      if query_params.state == 'ACTIVE':
        query['active'] = True
      else:
        query['active'] = False

    return query

  def update_user(self, id_user: str, user: UserUpdate) -> UserResponse:
    entity = self._update_entity(user=user)
    entity['updated_at'] = datetime.utcnow()
    entity = self._database.users.find_one_and_update(
        {'_id': id_user}, {'$set': entity})
    return UserResponse(**entity)

  def delete_user(self, id_user: str) -> UserResponse:
    entity = self._database.users.find_one_and_update(
        {'_id': id_user}, {'$set': {'active': False}})
    return UserResponse(**entity)

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
  def change_password(self, query_params: UserChangePassword) -> dict:
    print(query_params)
    return {}
