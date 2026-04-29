# @file app/helloworld/pages/boot.py
# @brief Boot page for the HelloWorld application

from __future__ import annotations

from PIL import Image, ImageDraw

from app.helloworld.draw_util import default_fonts
from app.helloworld.effects import Effect, Navigate
from app.helloworld.page_id import PageId
from services.buttonevent import ButtonEvent, ButtonEventKind

# @todo What information should be displayed on the boot page??
class BootPage:
    """Splash; first button press goes to the pet hub."""

    # Wait until button press to advance to pet home page
    def update(self, events: list[ButtonEvent], dt: float) -> list[Effect]:
        for ev in events:
            if ev.kind == ButtonEventKind.PRESS:
                return [Navigate(PageId.PET_HOME)]
        return []

    def render(self) -> Image.Image:
        img = Image.new("RGB", (240, 240), color = (20, 20, 30))
        draw = ImageDraw.Draw(img)
        font, small = default_fonts()
        draw.text(xy = (12, 90), text = "cyber-chain", fill=(200, 200, 255), font=font)
        draw.text(xy = (12, 130), text = "Press any button to start", fill=(180, 180, 200), font=small)

        return img
