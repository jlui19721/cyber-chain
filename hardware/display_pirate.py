from __future__ import annotations

from PIL import Image

# TODO build script??
from st7789 import ST7789, BG_SPI_CS_FRONT   # after install st7789 from third-party

def _pirate_audio_square_st7789() -> ST7789:
    """Match Pimoroni 'square' profile: 1.3\" 240x240, front Breakout Garden slot."""
    return ST7789(
        width=240,
        height=240,
        rotation=90,
        port=0,
        cs=BG_SPI_CS_FRONT,    # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
        dc=9,
        backlight=13,  # Breakout Garden: 18 for back slot, 19 for front slot.
                       # NOTE: Change this to 13 for Pirate Audio boards
        spi_speed_hz=80 * 1000 * 1000,
        offset_left=0,
        offset_top=0,
    )

class PirateDisplay:
    def __init__(self, disp: ST7789) -> None:
        self._disp = disp
        self._black = Image.new("RGB", (disp.width, disp.height), color = (0, 0, 0))
        # On Bootup, display a color screen
        self._disp.display(Image.new("RGB",(disp.width, disp.height), color = (137, 207, 240)))

    def clear(self) -> None:
        # Display a black screen
        self._disp.display(self._black)

    def show(self, frame: Image.Image) -> None:
        # Driver expects RGB and dimensions matching the hardware
        self._disp.display(frame)

    def shutdown(self) -> None:
        self._disp.set_backlight(False)

def make_pirate_display() -> PirateDisplay:
    disp = _pirate_audio_square_st7789()
    disp.begin()
    return PirateDisplay(disp)
