# @file app/state.py
# @brief Application state management
# AppState manages an application state for a button-controlled counter and label.
# It tracks the current frame index, a numeric counter, and which button was last pressed.
from dataclasses import dataclass
from typing import assert_never

from services.buttonevent import ButtonEvent, ButtonId, ButtonEventKind

@dataclass
class AppState:
    frame_idx: int = 0
    counter: int = 0
    last_label: str = "-"

    def report(self) -> str:
        return f"frame: {self.frame_idx}, counter: {self.counter}, last pressed: {self.last_label}"

    # @brief Update the application state based on ButtonEvents
    # @param dt - Time elapsed since the last update (s)
    # @param events - List of ButtonEvents since last update
    def update(self, events: list[ButtonEvent], _dt: float = 0.0) -> None:
        self.frame_idx += 1
        for ev in events:
            if ev.kind != ButtonEventKind.PRESS:
                continue

            if ev.button == ButtonId.A:
                self.counter += 1
                self.last_label = "A"
            elif ev.button == ButtonId.B:
                self.counter -= 1
                self.last_label = "B"
            elif ev.button == ButtonId.X:
                self.counter += 2
                self.last_label = "X"
            elif ev.button == ButtonId.Y:
                self.counter -= 2
                self.last_label = "Y"
            else:
                assert_never(ev.button)

    def reset(self) -> None:
        self.frame_idx = 0
        self.counter = 0
        self.last_label = "-"