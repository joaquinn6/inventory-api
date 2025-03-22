from pydantic import Field
from passlib.context import CryptContext

from models.entity import Entity

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Entity):
  email: str = Field(...)
  roles: list[str] = Field(...)
  full_name: str = Field(...)
  password: str = Field(default='')
  active: bool = Field(default=True)

  def new(self):
    self.email = self.email.lower()
    self.full_name = self.full_name.title()
    self.password = pwd_context.hash(self.password)
    self.active = True
    self.initialize()

  def update(self, new_item: "User"):
    self.on_update()
    self.full_name = new_item.full_name.title()
    self.active = new_item.active

  def change_password(self, new_password: str):
    self.on_update()
    self.password = pwd_context.hash(new_password)

  def to_report(self):
    user_dict = self.model_dump(by_alias=True)
    user_dict['roles'] = ", ".join(self.roles)
    user_dict['active'] = 'SI' if self.active else 'NO'
    user_dict['created_at'] = self.created_at.strftime("%d-%m-%Y %H:%M:%S")
    return user_dict

  def deactivate(self):
    self.on_update()
    self.active = False

  def activate(self):
    self.on_update()
    self.active = True


class UserInfo(Entity):
  email: str = Field(...)
  roles: list[str] = Field(...)
  full_name: str = Field(...)
  active: bool = Field(...)
