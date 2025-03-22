import re
from schemas.query_base import QueryBase


class SupplierQuery(QueryBase):
  name: str = None
  code: str = None
  contact_name: str = None
  contact_email: str = None
  contact_phone: str = None

  def get_query(self) -> dict:
    query = dict({})

    if self.name:
      query['name'] = re.compile(f'.*{self.name}.*', re.I)

    if self.code:
      query['code'] = re.compile(f'{self.code.upper()}.*', re.I)

    if self.contact_name:
      query['contact.name'] = re.compile(
          f'.*{self.contact_name}.*', re.I)

    if self.contact_email:
      query['contact.email'] = self.contact_email

    if self.contact_phone:
      query['contact.phone'] = self.contact_phone

    return query
