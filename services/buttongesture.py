# @file services/buttongesture.py
# @brief ButtonGesture class
# `ButtonGestureInput` processes a stream of `RawButtonEdge` events & produces `ButtonEvent` that correspond to button press or holds
# A button is registered as "held" if it is pressed for at least `hold_threshold_sec` seconds

from __future__ import annotations

import time
from dataclasses import dataclass, field

from services.buttonevent import ButtonEvent, ButtonEventKind, ButtonId, ButtonEdge, RawButtonEdge

@dataclass
class _ButtonTrack:
    down: bool = False
    down_at: float | None = None
    hold_emitted: bool = False

@dataclass
class ButtonGestureInput:
    """Consumes RawButtonEdge & elapsed time; produces semantic ButtonEvents"""

    hold_threshold_sec: float = 1.0
    _track: dict[_ButtonTrack, float] = field(default_factory=lambda: {b: _ButtonTrack() for b in ButtonId})

    # @brief Process a list of `RawButtonEdge` events & returns a list of `ButtonEvent`s
    # Keeps track of button states & emits `ButtonEvent` for press, release, & hold
    # @param raw - List of `RawButtonEdge` events
    # @param dt - Elapsed time since the last call
    def process(self, raw: list[RawButtonEdge], dt: float) -> list[ButtonEvent]:
        out: list[ButtonEvent] = []
        now = time.monotonic()

        for ev in raw:
            t = self._track[ev.button]
            if ev.edge == ButtonEdge.DOWN:  # On press
                t.down = True
                t.down_at = now
                t.hold_emitted = False
            else:                           # On release
                if t.down and t.down_at is not None and not t.hold_emitted:
                    out.append(ButtonEvent(ev.button, ButtonEventKind.PRESS))
                t.down = False
                t.down_at = None
                t.hold_emitted = False

        if dt > 0:
            for bid, t in self._track.items():
                if not t.down or t.down_at is None or t.hold_emitted:
                    continue
                if now - t.down_at > self.hold_threshold_sec:
                    out.append(ButtonEvent(bid, ButtonEventKind.HOLD))
                    t.hold_emitted = True

        return out
