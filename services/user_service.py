from datetime import datetime
import shortuuid
from fastapi import HTTPException

from core.auth import AuthService
from models.user_model import User, UserBase


class UserService():
  def __init__(self, database) -> None:
    self._database = database

  def create_user(self, user: UserBase) -> User:
    exist_user = self._database.users.find_one({'email': user.email})
    if exist_user:
      raise HTTPException(409, "Email ya posee una cuenta en el sistema")

    entity = self._create_entity(user=user)
    entity['created_at'] = datetime.utcnow()
    entity['updated_at'] = datetime.utcnow()
    self._database.users.insert_one(entity)
    user.id = entity['_id']
    return User(**user.model_dump())

  def _create_entity(self, user: UserBase) -> dict:
    return {
        '_id': shortuuid.uuid(),
        'email': user.email.lower(),
        'password': AuthService().get_password_hash(user.password),
        'roles': user.roles,
        'full_name': user.full_name
    }
