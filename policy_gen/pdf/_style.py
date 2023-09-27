from reportlab.lib.styles import StyleSheet1, getSampleStyleSheet
from reportlab.platypus import TableStyle

from ._fonts import INTER_REGULAR, SILKA_MEDIUM, register_fonts
from .colours import black, light_blue, white


def getPolicyStylesheet() -> StyleSheet1:
    """Returns a stylesheet object"""
    register_fonts()

    stylesheet = getSampleStyleSheet()

    stylesheet["BodyText"].fontName = INTER_REGULAR
    stylesheet["Heading1"].fontName = SILKA_MEDIUM

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
