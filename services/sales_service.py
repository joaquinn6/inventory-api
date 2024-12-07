
import re
from schemas.sales_schema import SalesQuery


class SaleService():
  def __init__(self, database) -> None:
    self._database = database

  def get_query(self, query_params: SalesQuery) -> tuple:
    pagination = self._get_pagination(query_params)
    query = self._get_query(query_params)
    return query, pagination

  def _get_query(self, _: SalesQuery) -> dict:
    query = dict({})

    return query

  def _get_pagination(self, query_params: SalesQuery) -> dict:
    return {
        'page': query_params.page,
        'limit': query_params.limit,
        'order': query_params.order,
        'sort': query_params.sort
    }
