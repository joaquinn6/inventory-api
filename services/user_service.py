from core import helpers_api
from core.auth import AuthService
from models.entity import PagedEntity
from models.user_model import User, UserInfo
from repositories.user_repository import UserRepository
from schemas.user_schema import UserQuery, UserChangePassword
from services.reports_service import ReportService


class UserService():
  def __init__(self) -> None:
    self._repo = UserRepository()

  def create_user(self, user: User) -> UserInfo:
    exist_user = self._repo.exist_by_email(user.email)
    if exist_user:
      helpers_api.raise_error_409('Email')

    user.new()
    self._repo.insert(user)
    return UserInfo.from_dict(user.model_dump(by_alias=True))

  def get_paged(self, query_params: UserQuery) -> PagedEntity:
    return self._repo.get_paged(query_params.get_query(), query_params.page, query_params.limit, query_params.sort, query_params.order)

  def update_user(self, exist: User, update: User) -> UserInfo:
    exist.update(update)
    self._repo.update_by_id(exist)
    return UserInfo.from_dict(exist.model_dump(by_alias=True))

  def delete_user(self, user: User) -> UserInfo:
    user.deactivate()
    self._repo.update_by_id(user)
    return UserInfo.from_dict(user.model_dump(by_alias=True))

  def active_user(self, user: User) -> UserInfo:
    user.activate()
    self._repo.update_by_id(user)
    return UserInfo.from_dict(user.model_dump(by_alias=True))

  def change_password(self, contract: UserChangePassword, user: User):
    auth_service = AuthService()
    if not auth_service.verify_password(contract.oldPassword, user.password):
      helpers_api.raise_error_422('Contraseña')

    user.change_password(contract.password)
    self._repo.update_by_id(user)

  def download_report(self, query_params: UserQuery) -> tuple:
    users = self._repo.get(
        query_params.get_query(), query_params.sort, query_params.order)
    columns = {
        'full_name': 'Nombre',
        'email': 'Email',
        'roles': 'Roles',
        'active': 'Activo',
        'created_at': 'Creado',
    }
    service = ReportService([{
        'data': [user.to_report() for user in users],
        'name': 'Proveedores',
        'columns': columns
    }])
    return service.generate_report()
