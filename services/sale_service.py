from datetime import datetime
import re
import shortuuid

from core import helpers_api
from models.sale_model import Sale
from schemas.sale_schema import SaleCreate, SaleQuery, Product, SaleWithDetail
from services.sale_detail_service import SaleDetailService


class SaleService():
  def __init__(self, database) -> None:
    self._database = database

  def create_sale(self, sale: SaleCreate) -> Sale:
    entity = self._create_entity(sale=sale)
    entity['_id'] = shortuuid.uuid()
    entity['created_at'] = datetime.utcnow()
    self._database.sales.insert_one(entity)
    self._create_details(entity['_id'], sale.products)
    return Sale(**entity)

  def get_sale_by_id(self, id_sale: str) -> SaleWithDetail:
    sale = self._database.sales.find_one({'_id': id_sale})
    if not sale:
      helpers_api.raise_error_404('Sale')
    detail = list(self._database.sale_details.find(
        {'sale_id': id_sale}))
    res = {
        'sale': sale,
        'detail': detail
    }
    return res

  def get_query(self, query_params: SaleQuery) -> tuple:
    pagination = self._get_pagination(query_params)
    query = self._get_query(query_params)
    return query, pagination

  def _create_entity(self, sale: SaleCreate) -> dict:
    return {
        'pay_type': sale.pay_type,
        'customer': sale.customer.capitalize(),
        'total_amount': sum([product.price * product.units for product in sale.products], 0)
    }

  def _get_query(self, query_params: SaleQuery) -> dict:
    query = dict({})

    if query_params.customer:
      query['customer'] = re.compile(f'.*{query_params.customer}.*', re.I)

    if query_params.pay_types:
      query['pay_type'] = {'$in': query_params.pay_types}

    if query_params.amount:
      if query_params.amount[1] != 10000:
        query['total_amount'] = {
            '$gte': query_params.amount[0], '$lte':  query_params.amount[1]}
      else:
        query['total_amount'] = {'$gte': query_params.amount[0]}
    return query

  def _get_pagination(self, query_params: SaleQuery) -> dict:
    return {
        'page': query_params.page,
        'limit': query_params.limit,
        'order': query_params.order,
        'sort': query_params.sort
    }

  def _create_details(self, id_sale: str, products: list[Product]):
    service = SaleDetailService(self._database)
    for product in products:
      service.create_detail(id_sale, product.id,
                            product.units, product.price)
