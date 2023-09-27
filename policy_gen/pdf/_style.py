from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle

from ._fonts import INTER_REGULAR, SILKA_MEDIUM, register_fonts
from .colours import light_blue, white


def getPolicyStylesheet() -> StyleSheet1:
    register_fonts()
    """Returns a stylesheet object"""
    stylesheet = StyleSheet1()

    stylesheet.add(
        ParagraphStyle(name="Normal", fontName=INTER_REGULAR, fontSize=12, leading=12)
    )

    stylesheet.add(
        ParagraphStyle(
            name="Paragraph",
            parent=stylesheet["Normal"],
            spaceAfter=inch / 4,
        ),
        alias="p",
    )

    stylesheet.add(
        ParagraphStyle(
            name="Heading1",
            parent=stylesheet["Normal"],
            fontName=SILKA_MEDIUM,
            fontSize=18,
            leading=22,
            spaceAfter=6,
        ),
        alias="h1",
    )

    stylesheet.add(
        ParagraphStyle(
            name="Title",
            parent=stylesheet["Normal"],
            fontName=SILKA_MEDIUM,
            fontSize=24,
            leading=22,
            spaceAfter=6,
        ),
        alias="title",
    )

    return stylesheet


def getChangeManagementTableStyle() -> TableStyle:
    register_fonts()
    """Table style for the change management table"""
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), light_blue),
            ("TEXTCOLOR", (0, 0), (-1, 0), (1, 1, 1)),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), INTER_REGULAR),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), white),
            ("GRID", (0, 0), (-1, -1), 1, (0, 0, 0)),
        ]
    )
