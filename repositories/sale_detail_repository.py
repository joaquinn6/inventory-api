from models.sale_detail_model import SaleDetail
from repositories.base import RepositoryBase


class SaleDetailRepository(RepositoryBase[SaleDetail]):

  def __init__(self) -> None:
    super().__init__('sale_details', SaleDetail.from_dict)
