from models.user_model import User
from repositories.base import RepositoryBase


class UserRepository(RepositoryBase[User]):

  def __init__(self) -> None:
    super().__init__('users', User.from_dict)

  def exist_by_email(self, email: str) -> bool:
    return self.get_by_email(email) is not None

  def get_by_email(self, email: str) -> User | None:
    return self.get_one({'email': email.lower()})
