from models.price_history_model import PriceHistory
from repositories.base import RepositoryBase


class PriceHistoryRepository(RepositoryBase[PriceHistory]):

  def __init__(self) -> None:
    super().__init__('prices_history', PriceHistory.from_dict)
