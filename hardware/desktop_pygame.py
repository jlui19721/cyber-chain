# @file hardware/desktop_pygame.py
# @brief Desktop stand-in for Pirate Audio display + buttons (Pygame)

from __future__ import annotations

import queue

import pygame
from PIL import Image

from services.buttonevent import ButtonEvent, ButtonId, ButtonEventKind

# Default: WASD → physical labels A,B,X,Y
DEFAULT_KEY_MAP: dict[ButtonId, int] = {}

def _default_keymap() -> dict[ButtonId, int]:
    return {
        pygame.K_w: ButtonId.A,
        pygame.K_a: ButtonId.B,
        pygame.K_s: ButtonId.X,
        pygame.K_d: ButtonId.Y,
    }

class DesktopDisplay:
    """Same contract as hardware.display_pirate.PirateDisplay: clear() + show() + shutdown()"""
    def __init__(self, width: int = 240, height: int = 240) -> None:
        pygame.display.init()
        self._screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("cyber-chain (desktop)")
        self._size = (width, height)

    def clear(self) -> None:
        self._screen.fill((0, 0, 0))

    def show(self, frame: Image.Image) -> None:
        if frame.size != self._size:
            print(f"Warning: Display size mismatch! Resizing from {frame.size} to {self._size}")
            frame = frame.resize(self._size)
        raw = frame.convert("RGB").tobytes()
        surf = pygame.image.frombuffer(raw, self._size, "RGB")
        self._screen.blit(surf, (0, 0))
        pygame.display.flip()

    def shutdown(self) -> None:
        pygame.display.quit()

class DesktopButtons:
    """Same contract as hardware.buttons_pirate.ButtonInput: poll() + shutdown()"""
    def __init__(
        self,
        key_map: dict[ButtonId, int] | None = None,
        *,
        stop_event=None
    )-> None:
        self._map = key_map if key_map is not None else _default_keymap()
        self._stop = stop_event

    def poll(self) -> list[ButtonEvent]:
        out: list[ButtonEvent] = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self._stop is not None:
                    self._stop.set()
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if self._stop is not None:
                    self._stop.set()
                continue
            elif event.type == pygame.KEYDOWN and event.key in self._map:
                out.append(ButtonEvent(self._map[event.key], ButtonEventKind.PRESS))
            elif event.type == pygame.KEYUP and event.key in self._map:
                out.append(ButtonEvent(self._map[event.key], ButtonEventKind.RELEASE))
        return out

    def shutdown(self) -> None:
        pass

def make_desktop(width: int = 240, height: int = 240, stop_event = None):
    pygame.init()
    key_map = _default_keymap()
    return DesktopDisplay(width, height), DesktopButtons(key_map, stop_event=stop_event)