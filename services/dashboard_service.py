from repositories.purchase_repository import PurchaseRepository
from repositories.sale_detail_repository import SaleDetailRepository


class DashboardService():
  def __init__(self) -> None:
    self._repo_sale_details = SaleDetailRepository()
    self._repo_purchase = PurchaseRepository()

  def get_dashboard(self) -> dict:
    res = {
        'top_10_products': self.get_top_10_products(),
        'top_3_suppliers': self.get_top_3_suppliers()
    }
    return res

  def get_top_10_products(self) -> list:
    pipeline = [
        {
            "$group": {
                "_id": "$product._id",
                "name": {"$first": "$product.name"},
                "value": {"$sum": "$units"}
            }
        },
        {
            "$sort": {"value": -1}
        },
        {
            "$limit": 10
        },
        {
            "$sort": {"name": 1}
        }
    ]
    results = self._repo_sale_details.aggregate(pipeline)
    return results

  def get_top_3_suppliers(self) -> list:
    pipeline = [
        {
            "$group": {
                "_id": "$supplier._id",
                "name": {"$first": "$supplier.name"},
                "value": {"$sum": "$total_amount"}
            }
        },
        {
            "$sort": {"value": -1}
        },
        {
            "$limit": 3
        },
        {
            "$sort": {"name": 1}
        }
    ]
    results = self._repo_purchase.aggregate(pipeline)
    return results
