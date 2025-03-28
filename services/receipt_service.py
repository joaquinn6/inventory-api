import base64
from io import BytesIO
from typing import List
from fpdf import FPDF, FontFace
from fpdf.enums import Align, TableBordersLayout
from PIL import Image

from models.sale_detail_model import SaleDetail
from models.sale_model import Sale
from repositories.config import ConfigRepository


class ReceiptService:
  def __init__(self, sale: Sale, details: List[SaleDetail]):
    self._sale = sale
    self._details = details
    config_repo = ConfigRepository()
    self._config = config_repo.get_one({})
    self._last_y = None

  def generate_receipt(self) -> bytes:
    pdf = FPDF(unit="mm", format=(48, 100 + len(self._details) * 15))
    pdf.add_page()
    pdf.set_margins(0, 5, 0)

    self._generate_header(pdf)
    pdf.set_font('Arial', size=8)
    self._generate_body(pdf)
    self._generate_footer(pdf)

    return pdf.output(dest='S')

  def _generate_header(self, pdf: FPDF):
    params = {
        # "line_height": 0.31,
        # "cell_fill_mode": "COLUMNS",  # !THIS
        "line_height": 0,
        "col_widths": [pdf.epw],
        "text_align": Align.C,
        "borders_layout": TableBordersLayout.NONE,
        "first_row_as_headings": False,
        "gutter_height": 0,
        "padding": 0
    }

    pdf.set_font('Arial', 'B', size=10)
    with pdf.table(**params) as table:
      if self._config.company.logo:
        row = table.row()
        logo = self.base64_to_image(self._config.company.logo, (100, 100))
        row.cell(img=logo, align=Align.C, img_fill_width=True,
                 style=FontFace(size_pt=0))

      row = table.row()
      row.cell(self._config.company.name, style=FontFace(size_pt=0))
      pdf.set_font('Arial', size=8)
      row = table.row()
      row.cell(self._config.company.slogan, style=FontFace(size_pt=0))

      row = table.row()
      row.cell(self._sale.created_at.strftime(
          '%d/%m/%Y'), style=FontFace(size_pt=0))

      row = table.row()
      row.cell(self._sale.id, style=FontFace(size_pt=0))

      row = table.row()
      row.cell(f'Usuario: {self._sale.user}')

    self._last_y = pdf.get_y()

  def _generate_footer(self, pdf: FPDF):
    params = {
        # "line_height": 0.0,
        # "cell_fill_mode": "COLUMNS",  # !THIS
        "col_widths": [pdf.epw],
        "text_align": Align.C,
        "borders_layout": TableBordersLayout.NONE,
        "first_row_as_headings": False,
        "gutter_height": 0,
        "padding": 0
    }
    pdf.dashed_line(0, self._last_y + 2, pdf.epw,
                    self._last_y + 2, dash_length=1, space_length=1)
    pdf.ln(1)

    with pdf.table(**params) as table:
      row = table.row()
      row.cell('"Gracias por su compra"')

  def _generate_body(self, pdf: FPDF):
    params = {
        # "cell_fill_mode": "COLUMNS",  # !THIS
        "line_height": 4,
        "col_widths": [pdf.epw * 0.6, pdf.epw * 0.4],
        "text_align": (Align.L, Align.R),
        "borders_layout": TableBordersLayout.NONE,
        "first_row_as_headings": True,
        "gutter_height": 0,
        "padding": 0
    }

    pdf.dashed_line(0, self._last_y + 2, pdf.epw,
                    self._last_y + 2, dash_length=1, space_length=1)
    pdf.ln(3)
    with pdf.table(**params) as table:
      for detail in self._details:
        row = table.row()
        row.cell("Producto")
        row.cell(f"Precio({self._config.currency.symbol})")

        row = table.row()
        row.cell(f"{detail.product.code} - {detail.product.name}", colspan=2)

        if detail.product.warranty.has_warranty:
          pdf.set_font('Arial', size=6, style='I')
          row = table.row()
          row.cell(
              f"Garantía: {detail.product.warranty.quantity} {detail.product.warranty.measure.return_description()}", colspan=2)
          pdf.set_font('Arial', size=8)

        row = table.row()
        row.cell(f"{detail.units} x {detail.unity_price}")
        row.cell(F"{detail.total_price}")
      pdf.set_font('Arial', 'B', size=10)
      row = table.row()
      row.cell(f"Total({self._config.currency.symbol}):")
      row.cell(f"{self._sale.total_amount}")

      pdf.set_font('Arial', size=8)
      row = table.row()
      row.cell(
          f"Pagado con: {self._sale.pay_type.return_description()}", colspan=2)
    self._last_y = pdf.get_y()

  def base64_to_image(self, base64_string: str, size: tuple = (100, 100)) -> Image:
    if "data:image" in base64_string:
      base64_string = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_bytes))
    return image.resize(size)
