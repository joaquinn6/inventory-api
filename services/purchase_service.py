from typing import List
from core import helpers_api
from models.entity import PagedEntity
from models.product_model import TrendTypes
from models.purchase_model import Purchase, Supplier
from models.price_history_model import PriceChangeType
from schemas.purchase_schema import PurchaseCreate, PurchaseQuery, Product, PurchaseWithDetail

from repositories.config import ConfigRepository
from repositories.product_repository import ProductRepository
from repositories.purchase_repository import PurchaseRepository
from repositories.supplier_repository import SupplierRepository
from repositories.purchase_detail_repository import PurchaseDetailRepository

from services.reports_service import ReportService
from services.price_history_service import PriceHistoryService
from services.purchase_detail_service import PurchaseDetailService


class PurchaseService():
  def __init__(self) -> None:
    self._repo = PurchaseRepository()
    self._repo_detail = PurchaseDetailRepository()
    self._repo_products = ProductRepository()
    self._repo_supplier = SupplierRepository()
    self._service_detail = PurchaseDetailService()
    self._service_price = PriceHistoryService()
    config_repo = ConfigRepository()
    self._config = config_repo.get_one({})

  def create_purchase(self, purchase: PurchaseCreate, user: str) -> Purchase:
    entity = self._create_entity(purchase=purchase)
    entity.new(user)
    self._repo.insert(entity)
    self._create_details(entity.id, purchase.products)
    self._update_products(purchase.products)
    return entity

  def get_purchase_by_id(self, id_purchase: str) -> PurchaseWithDetail:
    purchase = self._repo.get_by_id(id_purchase)
    if not purchase:
      helpers_api.raise_error_404('Compra')
    detail = self._repo_detail.get_by_purchase_id(id_purchase)
    return PurchaseWithDetail(purchase=purchase, detail=detail)

  def get_paged(self, query_params: PurchaseQuery) -> PagedEntity:
    return self._repo.get_paged(query_params.get_query(), query_params.page, query_params.limit, query_params.sort, query_params.order)

  def _create_entity(self, purchase: PurchaseCreate) -> Purchase:
    return Purchase(
        _id=None,
        created_at=None,
        updated_at=None,
        supplier=self._get_supplier(purchase.supplier_id),
        total_amount=sum([round(product.purchase_price * product.units, 2) for product in purchase.products], 0))

  def _get_supplier(self, supplier_id: str) -> Supplier:
    supplier = self._repo_supplier.get_by_id(supplier_id)
    if not supplier:
      helpers_api.raise_error_404('Proveedor')
    return Supplier(_id=supplier.id, code=supplier.code, name=supplier.name)

  def _update_products(self, products: List[Product]):
    for product in products:
      new_values = {
          "$set": {
              "purchase_price": product.purchase_price,
              "sale_price": product.sale_price
          },
          "$inc": {
              "stock": product.units
          }
      }
      entity = self._repo_products.get_by_id_and_update(
          product.id, new_values, 'before')
      if entity.purchase_price != product.purchase_price:
        self._service_price.create_history(
            product.id, product.purchase_price, PriceChangeType.PURCHASE)
        trend = TrendTypes.UPWARD
        if entity.purchase_price > product.purchase_price:
          trend = TrendTypes.FALLING
        self._repo_products.update_trend(product.id, trend)
      if entity.sale_price != product.sale_price:
        self._service_price.create_history(
            product.id, product.sale_price, PriceChangeType.SALE)

  def _create_details(self, id_purchase: str, products: List[Product]):
    for product in products:
      self._service_detail.create_detail(
          id_purchase, product.id,
          product.units, product.purchase_price)

  def download_report(self, query_params: PurchaseQuery, with_detail: bool = False) -> tuple:
    purchases = self._repo.get(
        query_params.get_query(), query_params.sort, query_params.order)
    columns = {
        '_id': 'Código',
        'created_at': 'Fecha',
        'supplier.code': 'Código proveedor',
        'supplier.name': 'Nombre proveedor',
        'total_amount': f'Total ({self._config.currency.symbol})',
    }
    purchases_report = [purchase.to_report() for purchase in purchases]
    total_amount = sum(purchase.total_amount for purchase in purchases)
    total_row = {'supplier.name': 'Total', 'total_amount': total_amount}
    purchases_report.append(total_row)

    sheets = list([])
    sheets.append({'data': purchases_report,
                  'name': 'Compras', 'columns': columns})
    if with_detail:
      self._make_details_sheets(sheets, purchases)
    service = ReportService(sheets)
    return service.generate_report()

  def _make_details_sheets(self, sheets: List, purchases: List[Purchase]):
    columns = {
        'product.code': 'Código producto',
        'product.name': 'Nombre',
        'units': 'Unidades',
        'unity_price': f'Precio unitario ({self._config.currency.symbol})',
        'total_price': f'Total ({self._config.currency.symbol})',
    }
    for purchase in purchases:
      if not purchase.id:
        continue
      name = purchase.id
      details = self._repo_detail.get_by_purchase_id(purchase.id)
      details_repo = [detail.to_report() for detail in details]
      total_price = sum(detail.total_price for detail in details)
      total_row = {'unity_price': 'Total', 'total_price': total_price}
      details_repo.append(total_row)
      sheets.append({'data': details_repo, 'name': name, 'columns': columns})
