from models.config_model import Config
from repositories.base import RepositoryBase


class ConfigRepository(RepositoryBase[Config]):

  def __init__(self) -> None:
    super().__init__('products', Config.from_dict)
