# @file app/helloworldapp.py
# @brief Hello-World application creating ButtonEvents & updating the AppState
from __future__ import annotations

import threading
import time
from typing import assert_never

from app.helloworld.effects import Effect, LogLine, Navigate, PauseMusic, StartMusic
from app.helloworld.page_id import PageId
from app.helloworld.pages.factory import PageFactory

from hardware.audio_output import AudioOutput

from services.buttongesture import ButtonGestureInput
from services.buttonevent import ButtonEvent, ButtonEventKind, ButtonId

FRAME_SECONDS = 1.0 / 30.0  # ~30 FPS; tune for Pi Zero vs Pi 4

class HelloWorldApp:
    # @brief Initialize the HelloWorldApp
    # @param display - `PirateDisplay` instance connected to ST7789 LCD display
    # @param buttons - `ButtonInput` instance connected to Pimoroni Pirate Audio buttons
    # @param quit_event - Event to signal the main loop to stop
    # @param frame_seconds - Target FPS (default: 30 FPS)
    def __init__(
        self,
        display,
        buttons,
        audio: AudioOutput,
        quit_event: threading.Event,
        frame_seconds: float = FRAME_SECONDS,
    ) -> None:
        # Internal members
        self._frame_seconds = frame_seconds
        self._stop = quit_event  # Event to signal the main loop to stop

        # External components
        self._display = display
        self._buttons = buttons
        self._gesture = ButtonGestureInput(hold_threshold_sec=1.0)
        self._audio = audio

        self._page_factory = PageFactory()
        self._page_id = PageId.BOOT
        self._page = self._page_factory.get(PageId.BOOT)

    # @brief Navigate to page `page_id`
    # @param page_id - Page identifier to navigate to
    def _go(self, page_id: PageId) -> None:
        self._page_id = page_id
        self._page = self._page_factory.get(page_id)

    # @brief Apply effects to the current page
    def _apply_effects(self, effects: list[Effect]) -> None:
        for effect in effects:
            match effect:
                case Navigate(page):
                    self._go(page)
                case LogLine(text):
                    print(text)
                case StartMusic(path):
                    self._audio.play_music_file(path)
                case PauseMusic():
                    self._audio.pause_music()
                case _:
                    assert_never(effect)

    # @brief Handle global events
    # Currently only supports HOLD-Y button to return to pet home from feature pages
    # @param events - List of ButtonEvents (per frame)
    def _global_events(self, events: list[ButtonEvent]) -> list[ButtonEvent]:
        """Hold Y returns to pet home from feature pages."""
        if self._page_id in (PageId.BOOT, PageId.PET_HOME):
            return events
        rest: list[ButtonEvent] = []
        for ev in events:
            if ev.kind == ButtonEventKind.HOLD and ev.button == ButtonId.Y:
                self._go(PageId.PET_HOME)
            else:
                rest.append(ev)
        return rest

    def run(self) -> None:
        self._display.clear()
        last = time.monotonic()

        while not self._stop.is_set():
            now = time.monotonic()
            dt = now - last
            last = now

            events = self._gesture.process(self._buttons.poll(), dt)   # Get raw button events & feed to gesture processor
            events = self._global_events(events)  # Handle global events

            effects = self._page.update(events, dt)
            self._apply_effects(effects)

            frame = self._page.render()
            self._display.show(frame)

            elapsed = time.monotonic() - now
            sleep_for = self._frame_seconds - elapsed
            if sleep_for < 0:
                print(
                    f"Warning: Frame took longer than target FPS! "
                    f"(Target: {self._frame_seconds:.4f}s, Actual: {elapsed:.4f}s)"
                )
            elif sleep_for > 0:
                self._stop.wait(timeout=sleep_for)

    def shutdown(self) -> None:
        self._stop.set()
        self._audio.shutdown()
