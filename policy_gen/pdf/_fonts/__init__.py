from pathlib import Path

from fontTools.ttLib import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLTTFont

FONT_PATH = Path(__file__).parent / "fonts"

INTER_REGULAR = "Inter Regular"
SILKA_MEDIUM = "Silka Medium"


def get_font_name(ttf_path):
    font = TTFont(ttf_path)
    namerecord = font["name"].getName(
        nameID=4, platformID=3, platEncID=1
    )  # Windows, Unicode
    if not namerecord:
        namerecord = font["name"].getName(
            nameID=4, platformID=3, platEncID=0
        )  # Windows, Symbol
    if not namerecord:
        namerecord = font["name"].getName(
            nameID=4, platformID=1, platEncID=0
        )  # Macintosh, Roman
    if not namerecord:
        return "Unknown Font"
    return namerecord.toUnicode()


__fonts_registered = False


def register_fonts():
    global __fonts_registered
    if __fonts_registered:
        return

    for font_file in FONT_PATH.glob("**/*.ttf"):
        font_name = get_font_name(font_file)
        try:
            pdfmetrics.registerFont(RLTTFont(font_name, font_file))
            print(f"{font_file.name}: {font_name}")
        except:
            print(f" * Failed to register font: {font_file.name}")

    __fonts_registered = True
