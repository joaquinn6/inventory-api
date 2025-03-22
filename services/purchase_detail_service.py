from models.purchase_detail_model import PurchaseDetail, Product
from repositories.product_repository import ProductRepository
from repositories.purchase_detail_repository import PurchaseDetailRepository


class PurchaseDetailService():
  def __init__(self) -> None:
    self._repo = PurchaseDetailRepository()
    self._repo_product = ProductRepository()

  def create_detail(self, id_purchase: str, product_id: str, units: int, price: float):
    entity = self._create_entity(id_purchase, product_id, units, price)
    entity.new()
    self._repo.insert(entity)

  def _create_entity(self, id_purchase: str, product_id: str, units: int, price: float) -> PurchaseDetail:
    return PurchaseDetail(
        _id=None,
        created_at=None,
        updated_at=None,
        purchase_id=id_purchase,
        product=self._get_product(product_id),
        units=units,
        unity_price=price,
        total_price=round(price * units, 2)
    )

  def _get_product(self, product_id: str) -> Product:
    entity = self._repo_product.get_by_id(product_id)
    return Product(
        _id=entity.id,
        name=entity.name,
        code=entity.code
    )
