from io import BytesIO
from typing import List
from reportlab.pdfgen import canvas

from models.sale_detail_model import SaleDetail
from models.sale_model import Sale


class ReceiptService:
  def __init__(self, sale: Sale, details: List[SaleDetail]):
    self._sale = sale
    self._details = details

  def generate_receipt(self) -> bytes:
    buffer = BytesIO()
    ancho_papel = 180
    alto_papel = 210 + len(self._details) * 30

    c = canvas.Canvas(buffer, pagesize=(ancho_papel, alto_papel))

    c.setFont("Helvetica", 10)
    y_position = alto_papel - 20  # Margen superior

    # Datos de la factura
    c.drawString(10, y_position, "Factura Electrónica")
    y_position -= 20
    c.drawString(10, y_position, "Empresa XYZ")
    y_position -= 20
    c.drawString(10, y_position, self._sale.created_at.strftime('%d/%m/%Y'))
    y_position -= 20
    c.drawString(10, y_position, f"Cliente: {self._sale.customer}")
    y_position -= 20
    c.drawString(10, y_position, "-" * 30)  # Línea separadora
    y_position -= 20

    # Productos
    for detail in self._details:
      c.drawString(
          10, y_position, f"{detail.product.code} {detail.product.name}")
      c.drawString(10, y_position-10,
                   f"x{detail.units} - C${detail.unity_price:.2f}    C${detail.total_price:.2f}")
      y_position -= 20

    c.drawString(10, y_position, "-" * 30)  # Línea separadora
    y_position -= 20

    # Total
    c.drawString(10, y_position, f"Total: ${self._sale.total_amount:.2f}")
    y_position -= 20

    c.save()
    buffer.seek(0)
    return buffer.read()
