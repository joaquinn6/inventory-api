from typing import List

from core import helpers_api
from models.entity import PagedEntity
from models.sale_model import Sale
from models.product_model import Product as ProductEntity
from repositories.product_repository import ProductRepository
from repositories.sale_detail_repository import SaleDetailRepository
from repositories.sale_repository import SaleRepository
from repositories.supplier_repository import SupplierRepository
from schemas.sale_schema import SaleCreate, SaleQuery, Product, SaleWithDetail
from services.price_history_service import PriceHistoryService
from services.sale_detail_service import SaleDetailService
from services.reports_service import ReportService


class SaleService():
  def __init__(self) -> None:
    self._repo = SaleRepository()
    self._repo_detail = SaleDetailRepository()
    self._repo_products = ProductRepository()
    self._repo_supplier = SupplierRepository()
    self._service_detail = SaleDetailService()
    self._service_price = PriceHistoryService()

  def create_sale(self, sale: SaleCreate) -> Sale:
    is_valid, products = self._valid_products(sale)
    if not is_valid:
      helpers_api.raise_error_400(
          f'No hay suficientes productos ({", ".join([product.name for product in products])}) para despachar la venta')
    entity = self._create_entity(sale=sale)
    entity.new()
    self._repo.insert(entity)
    self._create_details(entity.id, sale.products)
    self._update_products(sale.products)
    return entity

  def get_sale_by_id(self, id_sale: str) -> SaleWithDetail:
    sale = self._repo.get_by_id(id_sale)
    if not sale:
      helpers_api.raise_error_404('Venta')
    detail = self._repo_detail.get_by_sale_id(id_sale)
    return SaleWithDetail(sale=sale, detail=detail)

  def get_paged(self, query_params: SaleQuery) -> PagedEntity:
    return self._repo.get_paged(query_params.get_query(), query_params.page, query_params.limit, query_params.sort, query_params.order)

  def _create_entity(self, sale: SaleCreate) -> Sale:
    return Sale(
        _id=None,
        created_at=None,
        updated_at=None,
        pay_type=sale.pay_type,
        customer=sale.customer.title(),
        total_amount=sum([round(product.sale_price * product.units, 2) for product in
                          sale.products], 0)
    )

  def _create_details(self, id_sale: str, products: List[Product]):
    for product in products:
      self._service_detail.create_detail(
          id_sale, product.id,
          product.units, product.sale_price)

  def download_report(self, query_params: SaleQuery, with_detail: bool = False) -> tuple:
    sales = self._repo.get(
        query_params.get_query(),
        query_params.sort, query_params.order)
    columns = {
        '_id': 'Código',
        'created_at': 'Fecha',
        'customer': 'Cliente',
        'pay_type': 'Forma de pago',
        'total_amount': 'Cantidad total (C$)',
    }
    sales_report = [sale.to_report() for sale in sales]
    total_amount = sum(sale.total_amount for sale in sales)
    total_row = {'name': 'Total', 'total_amount': total_amount}
    sales_report.append(total_row)

    sheets = list([])
    sheets.append({'data': sales_report, 'name': 'Ventas', 'columns': columns})
    if with_detail:
      self._make_details_sheets(sheets, sales)
    service = ReportService(sheets)
    return service.generate_report()

  def _make_details_sheets(self, sheets: List, sales: List[Sale]):
    columns = {
        'product.code': 'Código producto',
        'product.name': 'Nombre',
        'units': 'Unidades',
        'unity_price': 'Precio unitario (C$)',
        'total_price': 'Total (C$)',
    }

    for sale in sales:
      if not sale.id:
        continue
      name = sale.id
      details = self._repo_detail.get_by_sale_id(sale.id)
      details_repo = [detail.to_report() for detail in details]
      total_price = sum(detail['total_price'] for detail in details)
      total_row = {'unity_price': 'Total', 'total_price': total_price}
      details_repo.append(total_row)
      sheets.append({'data': details_repo, 'name': name, 'columns': columns})

  def _valid_products(self, sale: SaleCreate) -> tuple[bool, List[ProductEntity] | None]:
    products = list([])
    for product in sale.products:
      query = {
          '_id': product.id,
          'stock': {'$lt': product.units}
      }
      entity = self._repo_products.get_one(query)
      if entity:
        products.append(entity)
    if len(products) > 0:
      return False, products
    return True, None

  def _update_products(self, products: List[Product]):
    for product in products:
      new_values = {
          "$inc": {
              "stock": -product.units
          }
      }
      self._repo_products.get_by_id_and_update(
          product.id, new_values, 'before')
