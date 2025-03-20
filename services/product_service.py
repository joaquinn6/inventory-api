import shortuuid
from core import helpers_api
from models.product_model import Product
from repositories.product_repository import ProductRepository
from repositories.price_history_repository import PriceHistoryRepository
from schemas.product_schema import ProductCreate, ProductQuery
from services.reports_service import ReportService


class ProductService():
  def __init__(self) -> None:
    self._repo = ProductRepository()
    self._repo_history = PriceHistoryRepository()

  def create_product(self, product: Product) -> Product:
    exist_product = self._repo.exist_by_code(product.code.upper())
    if exist_product:
      helpers_api.raise_error_409('Código')
    product.new()
    self._repo.insert(product)
    return product

  def update_product(self, exist: Product, update: Product) -> Product:
    exist_product = self._repo.get_by_code(update.code.upper())
    if exist_product and exist_product.id != exist.id:
      helpers_api.raise_error_409('Código')

    exist.update(update)

    self._repo.update_by_id(exist)
    return exist

  def get_paged(self, query_params: ProductQuery) -> tuple:
    # TODO: get y get paged order sort, limit... en repo
    return

  def _create_entity(self, product: ProductCreate) -> dict:
    return {
        '_id': shortuuid.uuid(),
        'name': product.name,
        'code': product.code.upper(),
        'categories': product.categories,
        'description': product.description.capitalize(),
        'purchase_price': 0.0,
        'sale_price': 0.0,
        'stock': 0
    }

  def download_report(self, query_params: ProductQuery) -> tuple:
    products = self._repo.get(query_params.get_query())
    columns = {
        'code': 'Código',
        'name': 'Nombre',
        'description': 'Descripción',
        'categories': 'Categorías',
        'purchase_price': 'Precio de compra',
        'sale_price': 'Precio de venta',
        'stock': 'Und.',
        'created_at': 'Creado',
    }
    service = ReportService(
        [{'data': [product.to_report() for product in products], 'name': 'Productos', 'columns': columns}])
    return service.generate_report()

  def get_prices_graph(self, id_product: str) -> dict:
    pipeline = [
        {
            "$match": {
                "type": "PURCHASE",
                "product_id": id_product
            }
        },
        {
            "$sort": {
                "date": 1
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {
                        "$year": "$date"
                    }
                },
                "prices": {
                    "$push": {
                        "date": {
                            "$dateToString": {
                                "format": "%d/%m",
                                "date": "$date"
                            }
                        },
                        "price": "$price"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "year": "$_id.year",
                "product_id": "$_id.product_id",
                "prices": 1
            }
        }
    ]
    results = self._repo_history.aggregate(pipeline)
    return list(results)
