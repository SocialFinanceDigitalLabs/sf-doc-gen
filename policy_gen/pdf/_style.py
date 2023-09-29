from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle

from ._fonts import INTER_REGULAR, SILKA_MEDIUM, register_fonts
from .colours import black, light_blue, white


def getPolicyStylesheet() -> StyleSheet1:
    """Returns a stylesheet object"""
    register_fonts()

    stylesheet = getSampleStyleSheet()

    TITLE = stylesheet["Title"]
    TITLE.fontName = SILKA_MEDIUM
    TITLE.fontSize = 24
    TITLE.alignment = TA_LEFT

    H1 = stylesheet["Heading1"]
    H1.fontName = SILKA_MEDIUM
    H1.fontSize = 14
    H1.spaceBefore = inch / 2

    BODY = stylesheet["BodyText"]
    BODY.fontName = INTER_REGULAR
    BODY.fontSize = 12
    BODY.leading = 16

    return stylesheet


def getChangeManagementTableStyle() -> TableStyle:
    register_fonts()
    """Table style for the change management table"""
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), light_blue),
            ("TEXTCOLOR", (0, 0), (-1, 0), (1, 1, 1)),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, 0), INTER_REGULAR),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), white),
            ("GRID", (0, 0), (-1, -1), 1, (0, 0, 0)),
        ]
    )
