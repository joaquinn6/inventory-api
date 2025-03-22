from models.price_history_model import PriceChangeType, PriceHistory
from repositories.price_history_repository import PriceHistoryRepository


class PriceHistoryService():
  def __init__(self) -> None:
    self._repo = PriceHistoryRepository()

  def create_history(self, product: str, price: float, type_price: PriceChangeType):
    entity = self._create_entity(product, price, type_price)
    entity.new()
    self._repo.insert(entity)

  def _create_entity(self, product: str, price: float, type_price: PriceChangeType) -> PriceHistory:
    return PriceHistory(
        _id=None,
        created_at=None,
        updated_at=None,
        product_id=product,
        type=type_price,
        price=price,
        date=None
    )
