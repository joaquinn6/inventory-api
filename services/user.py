from datetime import datetime
import shortuuid
from fastapi import HTTPException

from core.auth import AuthService


class UserService():
  def __init__(self, database) -> None:
    self._database = database

  def create_user(self, contract: dict):
    user = self._database.users.find_one({'email': contract['email']})
    if user:
      raise HTTPException(409, "Email ya posee una cuenta en el sistema")

    entity = self._create_entity(contract=contract)
    entity['created_at'] = datetime.utcnow()
    entity['updated_at'] = datetime.utcnow()
    self._database.users.insert_one(entity)
    return entity

  def _create_entity(self, contract: dict) -> dict:
    return {
        '_id': shortuuid.uuid(),
        'email': contract['email'].lower(),
        'password': AuthService().get_password_hash(contract['password']),
        'roles': contract['roles'],
        'full_name': contract['full_name']
    }
