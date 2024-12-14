from datetime import datetime
from pymongo import ReturnDocument
import pytz
import shortuuid

from core import helpers_api
from models.purchase_model import Purchase
from models.price_history_model import PriceChangeType
from schemas.purchase_schema import PurchaseCreate, PurchaseQuery, Product, PurchaseWithDetail
from services.purchase_detail_service import PurchaseDetailService
from services.price_history_service import PriceHistoryService


class PurchaseService():
  def __init__(self, database) -> None:
    self._database = database

  def create_purchase(self, purchase: PurchaseCreate) -> Purchase:
    entity = self._create_entity(purchase=purchase)
    entity['_id'] = shortuuid.uuid()
    entity['created_at'] = datetime.utcnow()
    self._database.purchases.insert_one(entity)
    self._create_details(entity['_id'], purchase.products)
    self._update_products(purchase.products)
    return Purchase(**entity)

  def get_purchase_by_id(self, id_purchase: str) -> PurchaseWithDetail:
    purchase = self._database.purchases.find_one({'_id': id_purchase})
    if not purchase:
      helpers_api.raise_error_404('Purchase')
    detail = list(self._database.purchase_details.find(
        {'purchase_id': id_purchase}))
    res = {
        'purchase': purchase,
        'detail': detail
    }
    return res

  def get_query(self, query_params: PurchaseQuery) -> tuple:
    pagination = self._get_pagination(query_params)
    query = self._get_query(query_params)
    return query, pagination

  def _create_entity(self, purchase: PurchaseCreate) -> dict:
    return {
        'supplier': self._get_supplier(purchase.supplier_id),
        'total_amount': sum([round(product.purchase_price * product.units, 2) for product in purchase.products], 0)
    }

  def _get_query(self, query_params: PurchaseQuery) -> dict:
    query = dict({})

    if query_params.date:
      query['created_at'] = {
          '$gte': query_params.date[0].astimezone(pytz.utc), '$lte':  query_params.date[1].astimezone(pytz.utc)}

    if query_params.supplier:
      query['supplier._id'] = query_params.supplier

    if query_params.amount:
      if query_params.amount[1] != 10000:
        query['total_amount'] = {
            '$gte': query_params.amount[0], '$lte':  query_params.amount[1]}
      else:
        query['total_amount'] = {'$gte': query_params.amount[0]}
    return query

  def _get_pagination(self, query_params: PurchaseQuery) -> dict:
    return {
        'page': query_params.page,
        'limit': query_params.limit,
        'order': query_params.order,
        'sort': query_params.sort
    }

  def _get_supplier(self, supplier_id: str) -> dict:
    supplier = self._database.suppliers.find_one({'_id': supplier_id})
    if not supplier:
      helpers_api.raise_error_404('Supplier')
    return {
        '_id': supplier['_id'],
        'code': supplier['code'],
        'name': supplier['name']
    }

  def _update_products(self, products: list[Product]):
    service = PriceHistoryService(self._database)
    for product in products:
      new_values = {
          "$set": {
              "purchase_price": product.purchase_price,
              "sale_price": product.sale_price
          },
          "$inc": {
              "stock": product.units
          }
      }
      entity = self._database.products.find_one_and_update(
          {'_id': product.id}, new_values, return_document=ReturnDocument.BEFORE)
      if entity['purchase_price'] != product.purchase_price:
        service.create_history(
            product.id, product.purchase_price, PriceChangeType.PURCHASE)
      if entity['sale_price'] != product.sale_price:
        service.create_history(
            product.id, product.sale_price, PriceChangeType.SALE)

  def _create_details(self, id_purchase: str, products: list[Product]):
    service = PurchaseDetailService(self._database)
    for product in products:
      service.create_detail(id_purchase, product.id,
                            product.units, product.purchase_price)
