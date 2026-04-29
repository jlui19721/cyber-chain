# @file app/helloworld/draw_util.py
# @brief Utility functions for drawing text on images

from __future__ import annotations
from PIL import ImageFont

# @brief Get the default fonts for the HelloWorld application
def default_fonts(
    large_px: int = 22, small_px: int = 16
) -> tuple[ImageFont.FreeTypeFont | ImageFont.ImageFont, ImageFont.FreeTypeFont | ImageFont.ImageFont]:
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", large_px)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", small_px)
        return font, small
    except OSError:
        font = ImageFont.load_default()
    return font, font
