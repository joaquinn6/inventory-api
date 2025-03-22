from typing import List
from models.purchase_detail_model import PurchaseDetail
from repositories.base import RepositoryBase


class PurchaseDetailRepository(RepositoryBase[PurchaseDetail]):

  def __init__(self) -> None:
    super().__init__('purchase_details', PurchaseDetail.from_dict)

  def get_by_purchase_id(self, id_purchase: str) -> List[PurchaseDetail]:
    return self.get({'purchase_id': id_purchase})
