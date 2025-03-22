import re
from typing import List
from pydantic import BaseModel, Field, field_validator
from schemas.query_base import QueryBase
from schemas.utils import divide_list


class UserLogin(BaseModel):
  email: str = Field(...)
  password: str = Field(...)


class UserChangePassword(BaseModel):
  password: str = Field(...)
  oldPassword: str = Field(...)


class UserQuery(QueryBase):
  full_name: str = None
  email: str = None
  roles: List[str] = None
  state: str = 'ALL'

  @field_validator("roles", mode="before")
  @classmethod
  def divide_roles(cls, value):
    return divide_list(value)

  def get_query(self) -> dict:
    query = dict({})
    if self.email:
      query['email'] = re.compile(f'.*{self.email}.*', re.I)

    if self.full_name:
      query['full_name'] = re.compile(f'.*{self.full_name}.*', re.I)

    if self.roles:
      query['roles'] = {'$in': self.roles}

    if self.state != 'ALL':
      if self.state == 'ACTIVE':
        query['active'] = True
      else:
        query['active'] = False

    return query
