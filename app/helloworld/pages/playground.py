# @file app/helloworld/pages/playground.py
# @brief

from __future__ import annotations

from dataclasses import dataclass, field
from typing import assert_never

from PIL import Image, ImageDraw

from app.helloworld.draw_util import default_fonts
from app.helloworld.effects import Effect, LogLine, PauseMusic, StartMusic
from services.buttonevent import ButtonEvent, ButtonEventKind, ButtonId

@dataclass
class PlaygroundState:
    frame_idx: int = 0
    counter: int = 0
    last_label: str = "-"
    last_event: str = "-"
    is_music_playing: bool = False
    current_music_file: str = ""

    def report(self) -> str:
        return (f"frame: {self.frame_idx}, counter: {self.counter}, "
                f"last pressed: {self.last_label}, last event: {self.last_event}, "
                f"is music playing: {self.is_music_playing}, current music file: {self.current_music_file}"
            )

    def update(self, events: list[ButtonEvent], dt: float = 0.0) -> list[Effect]:
        self.frame_idx += 1
        effects: list[Effect] = []
        for ev in events:
            if ev.kind == ButtonEventKind.RELEASE:
                continue
            if ev.kind == ButtonEventKind.HOLD:
                self.last_event = "HOLD"
                if ev.button == ButtonId.A:
                    if not self.is_music_playing:
                        self.current_music_file = "support/roses.mp3"
                        self.is_music_playing = True
                        effects.append(LogLine("Music starting..."))
                        effects.append(StartMusic(self.current_music_file))
                    self.counter += 1
                    self.last_label = "A"
                elif ev.button == ButtonId.B:
                    if self.is_music_playing:
                        self.is_music_playing = False
                        effects.append(LogLine("Music pausing..."))
                        effects.append(PauseMusic())
                    self.counter += 2
                    self.last_label = "B"
                elif ev.button == ButtonId.X:
                    self.counter += 3
                    self.last_label = "X"
                elif ev.button == ButtonId.Y:
                    self.counter += 4
                    self.last_label = "Y"
                else:
                    assert_never(ev.button)
            elif ev.kind == ButtonEventKind.PRESS:
                self.last_event = "PRESS"
                if ev.button == ButtonId.A:
                    self.counter -= 1
                    self.last_label = "A"
                elif ev.button == ButtonId.B:
                    self.counter -= 2
                    self.last_label = "B"
                elif ev.button == ButtonId.X:
                    self.counter -= 3
                    self.last_label = "X"
                elif ev.button == ButtonId.Y:
                    self.counter -= 4
                    self.last_label = "Y"
                else:
                    assert_never(ev.button)
            else:
                assert_never(ev.kind)
        return effects

    def reset(self) -> None:
        self.frame_idx = 0
        self.counter = 0
        self.last_label = "-"
        self.last_event = "-"
        self.is_music_playing = False
        self.current_music_file = ""

class PlaygroundPage:
    def __init__(self) -> None:
        self._state = PlaygroundState()

    def update(self, events: list[ButtonEvent], dt: float) -> list[Effect]:
        return self._state.update(events, dt)

    def render(self) -> Image.Image:
        state = self._state
        img = Image.new("RGB", size = (240, 240), color = (20, 20, 30))
        draw = ImageDraw.Draw(img)
        font, small = default_fonts()

        draw.text((12, 12), text="cyber-chain", fill=(200, 200, 255), font=font)
        draw.text((12, 50), text=f"counter: {state.counter}", fill=(255, 255, 255), font=font)
        draw.text((12, 70), text=f"last pressed: {state.last_label}", fill=(180, 180, 200), font=small)
        draw.text((12, 130), text=f"frame: {state.frame_idx}", fill=(120, 120, 140), font=small)
        draw.text((12, 150), text=f"last event: {state.last_event}", fill=(120, 120, 140), font=small)

        return img
