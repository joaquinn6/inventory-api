from datetime import datetime
import shortuuid

from models.price_history_model import PriceChangeType


class PriceHistoryService():
  def __init__(self, database) -> None:
    self._database = database

  def create_history(self, product_id: str, price: float, type_price: PriceChangeType):
    entity = self._create_entity(product_id, price, type_price)
    entity['created_at'] = datetime.utcnow()
    self._database.prices_history.insert_one(entity)

  def _create_entity(self, product_id: str, price: float, type_price: PriceChangeType) -> dict:
    return {
        '_id': shortuuid.uuid(),
        'product_id': product_id,
        'type': type_price,
        'price': price,
        'date': datetime.utcnow()
    }
