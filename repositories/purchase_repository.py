from models.purchase_model import Purchase
from repositories.base import RepositoryBase


class PurchaseRepository(RepositoryBase[Purchase]):

  def __init__(self) -> None:
    super().__init__('purchases', Purchase.from_dict)
