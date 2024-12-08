import re
import shortuuid
from datetime import datetime
from core import helpers_api
from schemas.supplier_schema import SupplierQuery, SupplierCreate, SupplierUpdate
from models.supplier_model import Supplier


class SupplierService():
  def __init__(self, database) -> None:
    self._database = database

  def create_supplier(self, supplier: SupplierCreate) -> Supplier:
    exist_supplier = self._database.supplier.find_one(
        {'code': supplier.code.upper()})
    if exist_supplier:
      helpers_api.raise_error_409('Code')

    entity = self._create_entity(supplier=supplier)
    entity['_id'] = shortuuid.uuid()
    entity['created_at'] = datetime.utcnow()
    entity['updated_at'] = datetime.utcnow()
    entity = self._database.supplier.insert_one(entity)
    return Supplier(**entity)

  def update_supplier(self, id_supplier: str, supplier: SupplierUpdate) -> Supplier:
    exist_supplier = self._database.suppliers.find_one(
        {'code': supplier.code.upper(), '_id': {'$ne': id_supplier}})
    if exist_supplier:
      helpers_api.raise_error_409('Code')

    entity = self._create_entity(supplier=supplier)
    entity['updated_at'] = datetime.utcnow()
    entity = self._database.suppliers.find_one_and_update(
        {'_id': id_supplier}, {'$set': entity})
    return Supplier(**entity)

  def get_query(self, query_params: SupplierQuery) -> tuple:
    pagination = self._get_pagination(query_params)
    query = self._get_query(query_params)
    return query, pagination

  def _create_entity(self, supplier: SupplierCreate) -> dict:
    return {
        'name': supplier.name.capitalize(),
        'code': supplier.code.upper(),
        'contact': {
            'name': supplier.contact.name.capitalize(),
            'phone': supplier.contact.phone,
            'email': supplier.contact.email
        }
    }

  def _get_query(self, query_params: SupplierQuery) -> dict:
    query = dict({})

    if query_params.name:
      query['name'] = re.compile(f'.*{query_params.name}.*', re.I)

    if query_params.code:
      query['code'] = re.compile(f'{query_params.code.upper()}.*', re.I)

    if query_params.contact_name:
      query['contact.name'] = re.compile(
          f'.*{query_params.contact_name}.*', re.I)

    if query_params.contact_email:
      query['contact.email'] = query_params.contact_email

    if query_params.contact_phone:
      query['contact.phone'] = query_params.contact_phone

    return query

  def _get_pagination(self, query_params: SupplierQuery) -> dict:
    return {
        'page': query_params.page,
        'limit': query_params.limit,
        'order': query_params.order,
        'sort': query_params.sort
    }
