from functools import cached_property
from pathlib import Path

from PIL import Image


class _Logo:
    def __init__(self, logo_path) -> None:
        self.logo_path = Path(logo_path)

    @cached_property
    def image(self):
        return Image.open(self.logo_path.as_posix())

    @property
    def width(self):
        return self.image.width

    @property
    def height(self):
        return self.image.height

    @property
    def aspect_ratio(self):
        return self.width / self.height

    def adjust_width_to_height(self, expected_height):
        return int(expected_height * self.aspect_ratio)

    def adjust_height_to_width(self, expected_width):
        return int(expected_width / self.aspect_ratio)


class SFLogo(_Logo):
    def __init__(self) -> None:
        super().__init__(Path(__file__).parent / "img/logo_white.png")
