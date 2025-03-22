from typing import List
from models.sale_detail_model import SaleDetail
from repositories.base import RepositoryBase


class SaleDetailRepository(RepositoryBase[SaleDetail]):

  def __init__(self) -> None:
    super().__init__('sale_details', SaleDetail.from_dict)

  def get_by_sale_id(self, id_sale: str) -> List[SaleDetail]:
    return self.get({'sale_id': id_sale})
