class DashboardService():
  def __init__(self, database) -> None:
    self._database = database

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
    results = self._database.sale_details.aggregate(pipeline)
    return list(results)

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
    results = self._database.purchases.aggregate(pipeline)
    return list(results)
