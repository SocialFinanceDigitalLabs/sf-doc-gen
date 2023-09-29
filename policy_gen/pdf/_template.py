from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

from ._fonts import INTER_BOLD, INTER_REGULAR
from ._sf_logo import SFLogo
from .colours import black, light_blue


class PolicyTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(
            self,
            filename,
            pagesize=A4,
            topMargin=1.5 * inch,
            leftMargin=inch / 2,
            rightMargin=inch / 2,
            **kwargs,
        )

        frame = Frame(
            self.leftMargin, self.bottomMargin, self.width, self.height, id="normal"
        )
        template = PageTemplate(id="policy", frames=frame, onPage=self.on_page)
        self.addPageTemplates([template])

        self._xobject = None
        self._pages = []

    def _endBuild(self):
        canvas = self.canv
        max_pagenum = max(self._pages)

        for page_number in self._pages:
            text = f"Page {page_number} of {max_pagenum}"
            canvas.beginForm(f"PageNumber{page_number}")
            canvas.setFont(INTER_REGULAR, 8)
            canvas.drawString(0.5 * inch, 0.75 * inch, text)
            canvas.endForm()

        BaseDocTemplate._endBuild(self)

    def on_page(self, canvas, _):
        canvas.saveState()

        # Logo
        logo_image = SFLogo()
        logo_height = 0.45 * inch
        logo_width = logo_image.adjust_width_to_height(logo_height)

        canvas.drawInlineImage(
            logo_image.image,
            0.5 * inch,
            10.7 * inch,
            width=logo_width,
            height=logo_height,
        )

        canvas.setFont(INTER_BOLD, 10)
        canvas.drawCentredString(4.135 * inch, 11 * inch, "Social Finance Limited")

        canvas.setFont(INTER_REGULAR, 10)
        canvas.drawCentredString(4.135 * inch, 10.8 * inch, "+44 (0)20 7770 6836")

        canvas.drawString(5.27 * inch, 11 * inch, "87 Vauxhall Walk, London SE11 5HJ")
        canvas.drawString(5.27 * inch, 10.8 * inch, "socialfinance.org.uk")
        canvas.setFont(INTER_REGULAR, 8)
        canvas.drawRightString(
            7.5 * inch,
            0.75 * inch,
            "Social Finance is authorised and regulated by the Financial Conduct Authority FCA No. 497568",
        )

        page_number = canvas.getPageNumber()
        self._pages.append(page_number)
        canvas.doForm(f"PageNumber{page_number}")

        if page_number == 1:
            # Draw the horizontal rule
            canvas.setStrokeColor(light_blue)
            canvas.setLineWidth(0.045 * inch)
            canvas.line(0.5 * inch, 10 * inch, 7.5 * inch, 10 * inch)

        canvas.setStrokeColor(black)
        canvas.setLineWidth(0.015 * inch)
        canvas.line(0.5 * inch, 1 * inch, 7.5 * inch, 1 * inch)

        canvas.restoreState()
