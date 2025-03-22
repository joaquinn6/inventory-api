from core import helpers_api
from models.entity import PagedEntity
from repositories.supplier_repository import SupplierRepository
from schemas.supplier_schema import SupplierQuery
from models.supplier_model import Supplier
from services.reports_service import ReportService


class SupplierService():
  def __init__(self) -> None:
    self._repo = SupplierRepository()

  def create_supplier(self, supplier: Supplier) -> Supplier:
    exist_supplier = self._repo.exist_by_code(supplier.code)
    if exist_supplier:
      helpers_api.raise_error_409('Código')
    supplier.new()
    self._repo.insert(supplier)
    return supplier

  def update_supplier(self, exist: Supplier, update: Supplier) -> Supplier:
    exist_supplier = self._repo.get_by_code(update.code.upper())
    if exist_supplier and exist_supplier.id != exist.id:
      helpers_api.raise_error_409('Código')

    exist.update(update)

    self._repo.update_by_id(exist)
    return exist

  def get_paged(self, query_params: SupplierQuery) -> PagedEntity:
    return self._repo.get_paged(query_params.get_query(), query_params.page, query_params.limit, query_params.sort, query_params.order)

  def download_report(self, query_params: SupplierQuery) -> tuple:
    suppliers = self._repo.get(
        query_params.get_query(), query_params.sort, query_params.order)
    columns = {
        'code': 'Código',
        'name': 'Nombre',
        'contact.name': 'Contacto',
        'contact.email': 'Email',
        'contact.phone': 'Teléfono',
        'created_at': 'Creado',
    }
    service = ReportService([{
        'data': [supplier.to_report() for supplier in suppliers],
        'name': 'Proveedores',
        'columns': columns
    }])
    return service.generate_report()
