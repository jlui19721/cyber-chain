# @file app/helloworldapp.py
# @brief Hello-World application creating ButtonEvents & updating the AppState
import threading
import time

from app.render import render
from app.state import AppState

FRAME_SECONDS = 1.0 / 30.0  # ~30 FPS; tune for Pi Zero vs Pi 4

class HelloWorldApp:
    # @brief Initialize the HelloWorldApp
    # @param display - `PirateDisplay` instance connected to ST7789 LCD display
    # @param buttons - `ButtonInput` instance connected to Pimoroni Pirate Audio buttons
    # @param frame_seconds - Target FPS (default: 30 FPS)
    def __init__(self, display, buttons, frame_seconds: float = FRAME_SECONDS):
        self._stop = threading.Event()   # Event to signal the main loop to stop

        self._display = display
        self._buttons = buttons
        self._frame_seconds = frame_seconds
        self._state = AppState()

    def run(self) -> None:
        self._display.clear()
        last = time.monotonic()

        while not self._stop.is_set():
            now = time.monotonic()
            dt = now - last
            last = now

            events = self._buttons.poll()
            self._state.update(events, dt)

            if events:  # if there are any events, update the state and display the frame
                print(self._state.report())

                frame = render(self._state)
                self._display.show(frame)

            elapsed = time.monotonic() - now
            sleep_for = self._frame_seconds - elapsed
            if sleep_for < 0:
                print(f"Warning: Frame took longer than target FPS! (Target: {self._frame_seconds:.4f}s, Actual: {elapsed:.4f}s)")
            elif sleep_for > 0:
                self._stop.wait(timeout=sleep_for)

    def shutdown(self) -> None:
        self._stop.set()
