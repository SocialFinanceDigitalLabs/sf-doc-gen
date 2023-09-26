from reportlab.platypus import Image
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Frame, PageTemplate, BaseDocTemplate
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import lightblue
from reportlab.platypus import Table, TableStyle
from pathlib import Path
from reportlab.lib.utils import ImageReader
from PIL import Image

project_root = Path(__file__).parent.parent
logo_path = project_root / "source/_static/logo_white.png"
build_path = project_root / "build"
build_path.mkdir(parents=True, exist_ok=True)


def get_resized_dimensions(image, expected_height):
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height
    new_width = int(expected_height * aspect_ratio)
    return new_width


class PolicyTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)

        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='normal')
        template = PageTemplate(id='test', frames=frame, onPage=self.on_page)
        self.addPageTemplates([template])

        self._xobject = None
        self._pages = []

    def _endBuild(self):
        canvas = self.canv
        max_pagenum = max(self._pages)

        for page_number in self._pages:
            text = f"Page {page_number} of {max_pagenum}"
            canvas.beginForm(f"PageNumber{page_number}")
            canvas.drawString(inch, 0.75 * inch, text)
            canvas.endForm()

        BaseDocTemplate._endBuild(self)


    def on_page(self, canvas, doc):
        canvas.saveState()
        page_number = canvas.getPageNumber()
        self._pages.append(page_number)
        canvas.doForm(f"PageNumber{page_number}")
        canvas.restoreState()



def create_pdf(paragraphs, filename):
    # Define a custom document with headers and footers


        # def add_header_footer(self, canvas, doc):
        #     # Header
        #     canvas.saveState()
            
        #     # Logo
        #     image = Image.open(logo_path.as_posix())
        #     height = 0.5 * inch
        #     width = get_resized_dimensions(image, height)

        #     canvas.drawInlineImage(image, 0.5*inch, 10.5*inch, width=width, height=height)
            
        #     canvas.setFont('Times-Bold', 12)
        #     canvas.drawCentredString(4.135 * inch, 11 * inch, "Company Name")
        #     canvas.drawString(6.27 * inch, 11 * inch, "1234 Company Address, City")
            
        #     # Footer
        #     canvas.setFont('Times-Roman', 10)
        #     canvas.drawString(inch, 0.75 * inch, f"Page {canvas.getPageNumber()} of ?")  # Updated to get actual page number
        #     canvas.drawCentredString(4.135 * inch, 0.75 * inch, "Compliance Statement")
        #     canvas.restoreState()

    doc = PolicyTemplate(filename, pagesize=A4)
    
    Story = []
    styles = getSampleStyleSheet()
    
    # Title and Version Control Table for First Page
    title = Paragraph("<u><b>Document Title</b></u>", styles['Title'])
    Story.append(title)
    data = [
        ["Version", "Date", "Author", "Changes Made"],
        ["1.0", "25/09/2023", "John Doe", "Initial version"],
    ]
    table = Table(data, colWidths=[1.5*inch]*4)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), (1, 1, 1)),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
    ]))
    Story.append(table)
    Story.append(Paragraph(" ", styles['Normal']))  # Some space after the table
    
    # Adding paragraphs without forced page breaks
    for para_text in paragraphs:
        p = Paragraph(para_text, styles['Normal'])
        Story.append(p)
        Story.append(PageBreak())
        
    doc.build(Story)

sample_text_v2 = [
    "<b>Lorem Ipsum</b> is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
    "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old.",
    "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable."
]

output_filename_v4 = build_path / "policy.pdf"
create_pdf(sample_text_v2, output_filename_v4.as_posix())
