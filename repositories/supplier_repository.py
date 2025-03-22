from models.supplier_model import Supplier
from repositories.base import RepositoryBase


class SupplierRepository(RepositoryBase[Supplier]):

  def __init__(self) -> None:
    super().__init__('suppliers', Supplier.from_dict)

  def exist_by_code(self, code: str) -> bool:
    return self.get_by_code(code) is not None

  def get_by_code(self, code: str) -> Supplier | None:
    return self.get_one({'code': code.upper()})
