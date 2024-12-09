import re
import shortuuid
from datetime import datetime
from core import helpers_api
from schemas.product_schema import ProductCreateResponse, ProductUpdateResponse, ProductCreate, ProductQuery


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
    return ProductCreateResponse(**entity)

  def update_product(self, id_product: str, product: ProductCreate) -> ProductUpdateResponse:
    exist_product = self._database.products.find_one(
        {'code': product.code.upper(), '_id': {'$ne': id_product}})
    if exist_product:
      helpers_api.raise_error_409('Code')

    entity = self._update_entity(product=product)
    entity['updated_at'] = datetime.utcnow()
    self._database.products.update_one({'_id': id_product}, {'$set': entity})
    entity['_id'] = id_product
    return ProductUpdateResponse(**entity)

  def get_query(self, query_params: ProductQuery) -> tuple:
    pagination = self._get_pagination(query_params)
    query = self._get_query(query_params)
    return query, pagination

  def _create_entity(self, product: ProductCreate) -> dict:
    return {
        '_id': shortuuid.uuid(),
        'name': product.name.capitalize(),
        'code': product.code.upper(),
        'categories': product.categories,
        'description': product.description.capitalize(),
        'purchase_price': 0.0,
        'sale_price': 0.0,
        'stock': 0
    }

  def _update_entity(self, product: ProductCreate) -> dict:
    return {
        'name': product.name.capitalize(),
        'code': product.code.upper(),
        'categories': product.categories,
        'description': product.description.capitalize(),
    }

  def _get_query(self, query_params: ProductQuery) -> dict:
    query = dict({})

    if query_params.name:
      query['name'] = re.compile(f'.*{query_params.name}.*', re.I)

    if query_params.code:
      query['code'] = re.compile(f'{query_params.code.upper()}.*', re.I)
    if query_params.categories:
      query['categories'] = {'$in': query_params.categories}
    if query_params.stock != 'ALL':
      if query_params.stock == 'NO_STOCK':
        query['stock'] = 0
      else:
        query['stock'] = {'$gt': 0}
    return query

  def _get_pagination(self, query_params: ProductQuery) -> dict:
    return {
        'page': query_params.page,
        'limit': query_params.limit,
        'order': query_params.order,
        'sort': query_params.sort
    }
