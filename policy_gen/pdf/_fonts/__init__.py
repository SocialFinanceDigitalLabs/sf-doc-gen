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


def check_font_flags(ttf_path):
    font = TTFont(ttf_path)

    names = font["name"].names

    for name in names:
        # Convert name string from bytes to str
        name_str = name.string.decode(name.getEncoding()) or ""
        print(
            f"PlatformID: {name.platformID}, Platform Encoding ID: {name.platEncID}, "
            f"Language ID: {name.langID}, Name ID: {name.nameID} - {name_str}"
        )

    # Accessing the 'OS/2' table
    print("\nOS/2 Table")
    os2_table = font["OS/2"]

    # Checking the fsSelection flags for bold and italic attributes
    is_bold = os2_table.fsSelection & 0x20  # Bold flag
    is_italic = os2_table.fsSelection & 0x01  # Italic flag

    print(f"Is Bold: {'Yes' if is_bold else 'No'}")
    print(f"Is Italic: {'Yes' if is_italic else 'No'}")

    print("\nHead Table")
    flags = font["head"].flags
    font_flags = {
        "baselineAtY0": flags & (1 << 0),
        "lsbAtX0": flags & (1 << 1),
        "deprecated": flags & (1 << 2),
        "force_ppm": flags & (1 << 3),
        "apple_tuned": flags & (1 << 4),
        "instructor": flags & (1 << 5),
        "apple_compatible": flags & (1 << 6),
        "x0_clears_left": flags & (1 << 7),
        "v0_clears_top": flags & (1 << 8),
        "instruct_H": flags & (1 << 9),
        "interpolate": flags & (1 << 10),
        "rounded": flags & (1 << 11),
        "monochrome": flags & (1 << 12),
        "multi_master": flags & (1 << 13),
        "extended_arrays": flags & (1 << 14),
    }

    for flag, value in font_flags.items():
        print(f"{flag}: {'Set' if value else 'Not set'}")


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

    check_font_flags(FONT_PATH / "Inter/Inter-Regular.ttf")
    check_font_flags(FONT_PATH / "Inter/Inter-Bold.ttf")

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

    print(fonts._tt2ps_map)
    print(fonts._ps2tt_map)

    print(pdfmetrics.getRegisteredFontNames())

    # for font_file in FONT_PATH.glob("**/*.ttf"):
    #     font_name = get_font_name(font_file)
    #     try:
    #         font = RLTTFont(font_name, font_file)
    #         pdfmetrics.registerFont(font)
    #         print(f"{font_file.name}: {font_name} - {ps2tt(font_name)}")
    #     except:
    #         print(f" * Failed to register font: {font_file.name}")

    __fonts_registered = True
