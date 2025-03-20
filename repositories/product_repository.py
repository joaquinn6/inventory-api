from models.product_model import Product
from repositories.base import RepositoryBase


class ProductRepository(RepositoryBase[Product]):

  def __init__(self) -> None:
    super().__init__('products', Product.from_dict)

  def exist_by_code(self, code: str) -> bool:
    return self.get_by_code(code) is not None

  def get_by_code(self, code: str) -> Product | None:
    return self.get_one({'code': code.upper()})
