import shortuuid
from datetime import datetime
from core import helpers_api
from models.price_history_model import PriceChangeType
from services.price_history_service import PriceHistoryService
from schemas.product_schema import ProductCreateResponse, ProductCreate


class ProductService():
  def __init__(self, database) -> None:
    self._database = database

  def create_product(self, product: ProductCreate) -> ProductCreateResponse:
    exist_product = self._database.products.find_one(
        {'code': product.code.upper()})
    if exist_product:
      helpers_api.raise_error_409('Code')

    entity = self._create_entity(product=product)
    entity['created_at'] = datetime.utcnow()
    entity['updated_at'] = datetime.utcnow()
    self._database.products.insert_one(entity)
    price_service = PriceHistoryService(self._database)
    price_service.create_history(
        entity['_id'], entity['purchase_price'], PriceChangeType.PURCHASE, 'New product')
    price_service.create_history(
        entity['_id'], entity['purchase_price'], PriceChangeType.SALE, 'New product')
    return ProductCreateResponse(id=entity['_id'], **entity)

  def _create_entity(self, product: ProductCreate) -> dict:
    return {
        '_id': shortuuid.uuid(),
        'name': product.name.capitalize(),
        'code': product.code.upper(),
        'categories': product.categories,
        'description': product.description.capitalize(),
        'purchase_price': product.purchase_price,
        'sale_price': product.sale_price,
        'stock': 0
    }
