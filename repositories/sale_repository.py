from models.sale_model import Sale
from repositories.base import RepositoryBase


class SaleRepository(RepositoryBase[Sale]):

  def __init__(self) -> None:
    super().__init__('sales', Sale.from_dict)
