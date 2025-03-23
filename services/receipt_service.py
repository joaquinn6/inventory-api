from typing import List
from fpdf import FPDF
from fpdf.enums import Align, TableBordersLayout

from models.sale_detail_model import SaleDetail
from models.sale_model import Sale


class ReceiptService:
  def __init__(self, sale: Sale, details: List[SaleDetail]):
    self._sale = sale
    self._details = details

  def generate_receipt(self) -> bytes:
    pdf = FPDF(unit="mm", format=(48, 60 + len(self._details) * 15))
    pdf.add_page()
    pdf.set_margins(0, 0, 0)

    self._generate_header(pdf)
    pdf.set_font('Arial', size=8)
    self._generate_body(pdf)
    self._generate_footer(pdf)

    return pdf.output(dest='S')

  def _generate_header(self, pdf: FPDF):
    pdf.set_font('Arial', 'B', size=10)
    with pdf.table(col_widths=[pdf.epw], text_align=Align.C, borders_layout=TableBordersLayout.NONE, first_row_as_headings=False, gutter_height=0, padding=0) as table:
      row = table.row()
      row.cell('Empresa fantasma', )
      pdf.set_font('Arial', size=8)

      row = table.row()
      row.cell(self._sale.created_at.strftime('%d/%m/%Y'))

      row = table.row()
      row.cell(self._sale.id)

  def _generate_footer(self, pdf: FPDF):
    with pdf.table(col_widths=[pdf.epw], text_align=Align.C, borders_layout=TableBordersLayout.NONE, first_row_as_headings=False, gutter_height=0, padding=0) as table:
      row = table.row()
      row.cell('Gracias por su compra')

  def _generate_body(self, pdf: FPDF):
    with pdf.table(col_widths=[pdf.epw * 0.7, pdf.epw * 0.3], text_align=(Align.L, Align.R), borders_layout=TableBordersLayout.NONE, first_row_as_headings=True, gutter_height=0, padding=0) as table:
      for detail in self._details:
        row = table.row()
        row.cell("Producto")
        row.cell("Precio")

        row = table.row()
        row.cell(f"{detail.product.code} - {detail.product.name}")
        row.cell(f"C${detail.unity_price}")

        row = table.row()
        row.cell(f"{detail.units} und")
        row.cell(F"C${detail.total_price}")

      row = table.row()
      row.cell("Total:")
      row.cell(f"{self._sale.total_amount}")
