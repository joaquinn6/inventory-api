from bson import ObjectId
from models.product_model import Product, TrendTypes
from repositories.base import RepositoryBase


class ProductRepository(RepositoryBase[Product]):

  def __init__(self) -> None:
    super().__init__('products', Product.from_dict)

  def exist_by_code(self, code: str) -> bool:
    return self.get_by_code(code) is not None

  def get_by_code(self, code: str) -> Product | None:
    return self.get_one({'code': code.upper()})

  def update_trend(self, id_product: str, trend: TrendTypes):
    self._collection.update_one(
        {'_id': ObjectId(id_product)}, {'$set': {'trend': trend}})
