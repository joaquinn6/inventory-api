from models.sale_detail_model import SaleDetail, Product
from repositories.product_repository import ProductRepository
from repositories.sale_detail_repository import SaleDetailRepository


class SaleDetailService():
  def __init__(self) -> None:
    self._repo = SaleDetailRepository()
    self._repo_product = ProductRepository()

  def create_detail(self, id_sale: str, product_id: str, units: int, price: float):
    entity = self._create_entity(id_sale, product_id, units, price)
    entity.new()
    self._repo.insert(entity)

  def _create_entity(self, id_sale: str, product_id: str, units: int, price: float) -> SaleDetail:
    return SaleDetail(
        _id=None,
        created_at=None,
        updated_at=None,
        sale_id=id_sale,
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
        code=entity.code,
        warranty=entity.warranty
    )
