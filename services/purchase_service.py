
import re
from schemas.purchases_schema import PurchasesQuery

class PurchaseQuery():
  def __init__(self, database) -> None:
    self._database = database

  def get_query(self, query_params: PurchasesQuery) -> tuple:
    pagination = self._get_pagination(query_params)
    query = self._get_query(query_params)
    return query, pagination

  def _get_query(self, query_params: PurchasesQuery) -> dict:
    query = dict({})

    if query_params.name:
      query['name'] = re.compile(f'.*{query_params.name}.*', re.I)
    return query