from pathlib import Path

from fontTools.ttLib import TTFont
from reportlab.lib import fonts
from reportlab.lib.fonts import addMapping, ps2tt, tt2ps
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLTTFont

FONT_PATH = Path(__file__).parent / "fonts"

INTER_REGULAR = "Inter-Regular"
INTER_BOLD = "Inter-Bold"
SILKA_MEDIUM = "Silka-Regular"
__fonts_registered = False


def register_fonts():
    global __fonts_registered
    if __fonts_registered:
        return

    pdfmetrics.registerFont(
        RLTTFont(INTER_REGULAR, FONT_PATH / "Inter/Inter-Regular.ttf")
    )
    pdfmetrics.registerFont(RLTTFont(INTER_BOLD, FONT_PATH / "Inter/Inter-Bold.ttf"))
    pdfmetrics.registerFont(
        RLTTFont("Inter-Light", FONT_PATH / "Inter/Inter-Light.ttf")
    )
    pdfmetrics.registerFont(
        RLTTFont("Inter-SemiBold", FONT_PATH / "Inter/Inter-SemiBold.ttf")
    )

    pdfmetrics.registerFont(RLTTFont("Inter-Italic", FONT_PATH / "Arial-Italic.ttf"))

    pdfmetrics.registerFont(
        RLTTFont(
            "Silka-Regular",
            FONT_PATH
            / "Silka-Complete-Webfont/Silka-Roman-Webfont/silka-medium-webfont.ttf",
        )
    )
    pdfmetrics.registerFont(
        RLTTFont(
            "Silka-Bold",
            FONT_PATH
            / "Silka-Complete-Webfont/Silka-Roman-Webfont/silka-bold-webfont.ttf",
        )
    )
    pdfmetrics.registerFont(
        RLTTFont(
            "Silka-Italic",
            FONT_PATH
            / "Silka-Complete-Webfont/Silka-Italic-Webfont/silka-regularitalic-webfont.ttf",
        )
    )
    pdfmetrics.registerFont(
        RLTTFont(
            "Silka-BoldItalic",
            FONT_PATH
            / "Silka-Complete-Webfont/Silka-Italic-Webfont/silka-bolditalic-webfont.ttf",
        )
    )

    fonts.addMapping("inter", 0, 0, "Inter-Regular")
    fonts.addMapping("inter", 1, 0, "Inter-Bold")
    fonts.addMapping("inter", 0, 1, "Inter-Italic")
    fonts.addMapping("inter", 1, 1, "Inter-SemiBold")

    fonts.addMapping("silka", 0, 0, "Silka-Regular")
    fonts.addMapping("silka", 1, 0, "Silka-Bold")
    fonts.addMapping("silka", 0, 1, "Silka-Italic")
    fonts.addMapping("silka", 1, 1, "Silka-BoldItalic")

    __fonts_registered = True
