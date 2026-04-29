# @file app/helloworld/pages/pet_home.py
# @brief Pet home page for the HelloWorld application

from __future__ import annotations

from PIL import Image, ImageDraw

from app.helloworld.draw_util import default_fonts
from app.helloworld.effects import Effect, Navigate
from app.helloworld.page_id import PageId
from services.buttonevent import ButtonEvent, ButtonEventKind, ButtonId

# @todo Eventually display a graphic/animation of pet on this page
# This page is used to navigate to the other pages after the boot page.
# The pet should be displayed on this page & perform actions (ie. wag tail, play with toy, etc.)
# As buttons are pressed to navigate to other pages, the pet should "walk" towards the other pages.
# It would be helpful to display on screen which button press would navigate to which page
class PetHomePage:
    f"""Pet Hub: One button per destination page."""

    def update(self, events: list[ButtonEvent], dt: float) -> list[Effect]:
        for ev in events:
            if ev.kind != ButtonEventKind.PRESS:
                continue

            match ev.button:
                case ButtonId.A:
                    return [Navigate(PageId.PLAYGROUND)]
                case ButtonId.B:
                    return [Navigate(PageId.MUSIC)]
                case ButtonId.X:
                    return [Navigate(PageId.VOICE)]
                case ButtonId.Y:
                    return [Navigate(PageId.NOTES)]
                case _:
                    assert_never(ev.button)
        return []

    def render(self) -> Image.Image:
        img = Image.new("RGB", (240, 240), color = (20, 20, 30))
        draw = ImageDraw.Draw(img)
        font, small = default_fonts()
        draw.text(xy = (12, 12), text = "Pet Home", fill = (220, 220, 255), font=font)
        y = 52
        for line in (
            "A: Playground",
            "B: Music",
            "X: Voice",
            "Y: Notes",
        ):
            draw.text(xy = (12, y), text = line, fill = (180, 180, 200), font=small)
            y += 20
        return img
