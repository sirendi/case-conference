from fpdf import FPDF
import io
from datetime import datetime


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.left_margin, self.top_margin, self.right_margin = 15, 15, 15
        self.set_margins(self.left_margin, self.top_margin, self.right_margin)

    def header(self) -> None:
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'AI Medical Review', 0, 1, 'C')

        self.set_font('Arial', '', 10)
        self.cell(0, 10, f'Date: {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')

    def footer(self) -> None:
        # Footer position
        self.set_y(-20)

        # Confidentiality Notice
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, 'Confidential: For internal use only', 0, 1, 'C')

        # Page number
        self.cell(0, 5, f'Page {self.page_no()}', 0, 0, 'C')

    def add_page(self, orientation='') -> None:
        super().add_page(orientation)
        self.set_line_width(0.1)


def create_pdf(content: str) -> io.BytesIO:
    content = content.replace('\u2019', "'")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    effective_page_width = pdf.w - pdf.left_margin - pdf.right_margin
    pdf.multi_cell(effective_page_width, 10, content)

    pdf_output = io.BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin-1'))
    pdf_output.seek(0)

    return pdf_output
