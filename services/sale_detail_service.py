from datetime import datetime
import shortuuid


class SaleDetailService():
  def __init__(self, database) -> None:
    self._database = database

  def create_detail(self, id_sale: str, product_id: str, units: int, price: float):
    entity = self._create_entity(id_sale, product_id, units, price)
    entity['_id'] = shortuuid.uuid()
    entity['created_at'] = datetime.utcnow()
    self._database.sale_details.insert_one(entity)

  def _create_entity(self, id_sale: str, product_id: str, units: int, price: float) -> dict:
    return {
        'sale_id': id_sale,
        'product': self._get_product(product_id),
        'units': units,
        'unity_price': price,
        'total_price': price * units,
    }

  def _get_product(self, product_id: str) -> dict:
    entity = self._database.products.find_one({'_id': product_id})
    return {
        '_id': entity['_id'],
        'code': entity['code'],
        'name': entity['name'],
    }
