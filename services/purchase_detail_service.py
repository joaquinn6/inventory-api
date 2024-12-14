from datetime import datetime
import shortuuid


class PurchaseDetailService():
  def __init__(self, database) -> None:
    self._database = database

  def create_detail(self, id_purchase: str, product_id: str, units: int, price: float):
    entity = self._create_entity(id_purchase, product_id, units, price)
    entity['_id'] = shortuuid.uuid()
    entity['created_at'] = datetime.utcnow()
    self._database.purchase_details.insert_one(entity)

  def _create_entity(self, id_purchase: str, product_id: str, units: int, price: float) -> dict:
    return {
        'purchase_id': id_purchase,
        'product': self._get_product(product_id),
        'units': units,
        'unity_price': price,
        'total_price': round(price * units, 2),
    }

  def _get_product(self, product_id: str) -> dict:
    entity = self._database.products.find_one({'_id': product_id})
    return {
        '_id': entity['_id'],
        'code': entity['code'],
        'name': entity['name'],
    }
