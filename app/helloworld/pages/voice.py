# @file app/helloworld/pages/voice.py
# @brief Voice page for the HelloWorld application

from __future__ import annotations

from PIL import Image, ImageDraw

from typing import assert_never

from app.helloworld.draw_util import default_fonts
from app.helloworld.effects import Effect, Navigate
from app.helloworld.page_id import PageId
from services.buttonevent import ButtonEvent, ButtonEventKind, ButtonId

# @todo Is there a way to playback voice notes?? Record them back to notes page??
class VoicePage:
    def update(self, _events: list[ButtonEvent], _dt: float) -> list[Effect]:
        for ev in _events:
            if ev.kind == ButtonEventKind.RELEASE:
                continue
            elif ev.kind == ButtonEventKind.HOLD:
                if ev.button == ButtonId.Y:
                    return [Navigate(PageId.PET_HOME)]
                else:
                    assert_never(ev.button)
            elif ev.kind == ButtonEventKind.PRESS:
                if ev.button == ButtonId.Y:
                    return [Navigate(PageId.PET_HOME)]
                else:
                    assert_never(ev.button)
            else:
                assert_never(ev.kind)
        return []

    def render(self) -> Image.Image:
        img = Image.new("RGB", size = (240, 240), color = (20, 20, 30))
        draw = ImageDraw.Draw(img)
        font, small = default_fonts()

        draw.text((12, 80), "Voice", fill=(230, 230, 255), font=font)
        draw.text((12, 120), "TBD", fill=(150, 150, 170), font=small)
        draw.text((12, 200), "Hold Y: home", fill=(100, 100, 120), font=small)

        return img
