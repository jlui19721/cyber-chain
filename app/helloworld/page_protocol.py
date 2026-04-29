# @file app/helloworld/page_protocol.py
# @brief

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from PIL import Image

if TYPE_CHECKING:
    from app.helloworld.effects import Effect
    from services.buttonevent import ButtonEvent

@runtime_checkable
class Page(Protocol):
    def update(self, events: list[ButtonEvent], dt: float) -> list[Effect]: ...
    def render(self) -> Image.Image: ...
