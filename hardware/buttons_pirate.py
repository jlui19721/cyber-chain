import queue
from typing import List

import RPi.GPIO as GPIO

from services.buttonevent import ButtonEvent, ButtonId, ButtonEventKind

# https://github.com/pimoroni/pirate-audio/blob/master/build%20your%20own/read_gpio_pins.py
# The buttons on Pirate Audio are connected to pins 5, 6, 16 and 24
PINS: dict[ButtonId, int] = {
    ButtonId.A: 5,
    ButtonId.B: 6,
    ButtonId.X: 16,
    ButtonId.Y: 24,
}

class ButtonInput:
    def __init__(
        self,
        event_queue: "queue.Queue[ButtonEvent]",
        buttons: List["Button"],
        ) -> None:
        self._q = event_queue
        self._buttons = buttons  # Keep refs for teardown

    def poll(self) -> List[ButtonEvent]:
        out: List[ButtonEvent] = []
        while True:
            try:
                out.append(self._q.get_nowait())
            except queue.Empty:
                break
        return out

    def shutdown(self) -> None:
        for b in self._buttons:
            b.teardown()
        self._buttons.clear()

        while True:
            try:
                self._q.get_nowait()
            except queue.Empty:
                break

        for pin in PINS.values():
            GPIO.cleanup(pin)

class Button:
    def __init__(
        self,
        button_id: ButtonId,
        bcm_pin: int,
        event_queue: "queue.Queue[ButtonEvent]",
        *,
        # Buttons connect to ground when pressed. so we should set them up
        # with a "PULL UP", which weakly pulls the input signal to 3.3V
        pull_up_down=GPIO.PUD_UP,
        # Bounce time is the amount of time to wait for the button to settle
        # after a press or release
        bounce_ms: int = 50,
    ) -> None:
        self._id = button_id
        self._pin = bcm_pin
        self._q = event_queue
        self._pull = pull_up_down
        self._bounce = bounce_ms

    def setup(self) -> None:
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=self._pull)
        GPIO.add_event_detect(
            self._pin,
            GPIO.BOTH,  # Trigger on both rising & falling edges
            callback=self._on_edge,
            bouncetime=self._bounce,
        )

    def _on_edge(self, channel: int) -> None:
        # Pull-up: pressed reads LOW (0). If your board is active-high, flip this.
        pressed = GPIO.input(channel) == GPIO.LOW
        kind = ButtonEventKind.PRESS if pressed else ButtonEventKind.RELEASE
        self._q.put(ButtonEvent(self._id, kind))

    def teardown(self) -> None:
        GPIO.remove_event_detect(self._pin)

# Initialize the buttons on the Pimoroni Pirate Audio board
def make_pirate_buttons() -> ButtonInput:
    GPIO.setmode(GPIO.BCM)
    q: "queue.Queue[ButtonEvent]" = queue.Queue()
    buttons = [Button(bid, PINS[bid], q) for bid in PINS]
    for b in buttons:
        b.setup()
    # Keep references if you need teardown later
    return ButtonInput(q, buttons)
