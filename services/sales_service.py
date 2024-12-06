
import re
from schemas.sales_schema import SalesQuery

class SaleService():
  def __init__(self, database) -> None:
    self._database = database

  def get_query(self, query_params: SalesQuery) -> tuple:
    pagination = self._get_pagination(query_params)
    query = self._get_query(query_params)
    return query, pagination

  def _get_query(self, query_params: SalesQuery) -> dict:
    query = dict({})

    if query_params.name:
      query['name'] = re.compile(f'.*{query_params.name}.*', re.I)
    return query