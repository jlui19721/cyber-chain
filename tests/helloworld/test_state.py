# @file tests/test_state.py
# @brief Focus on testing the `AppState` class
import pytest

from app.helloworld.state import AppState
from services.buttonevent import ButtonEvent, ButtonEventKind, ButtonId

@pytest.mark.parametrize(
    "button_id, expected_delta , expected_label",
    [
        (ButtonId.A, -1, "A"),
        (ButtonId.B, -2, "B"),
        (ButtonId.X, -3, "X"),
        (ButtonId.Y, -4, "Y"),
    ]
)
def test_button_press(button_id, expected_delta, expected_label):
    state = AppState()

    initial = state.counter
    event = ButtonEvent(button_id, ButtonEventKind.PRESS)
    state.update([event])

    assert state.counter == initial + expected_delta
    assert state.last_label == expected_label
    assert state.frame_idx == 1

@pytest.mark.parametrize(
    "button_id, expected_delta, expected_label",
    [
        (ButtonId.A, 1, "A"),
        (ButtonId.B, 2, "B"),
        (ButtonId.X, 3, "X"),
        (ButtonId.Y, 4, "Y"),
    ]
)
def test_button_hold(button_id, expected_delta, expected_label):
    state = AppState()
    event = ButtonEvent(button_id, ButtonEventKind.HOLD)
    state.update([event])

    assert state.counter == expected_delta
    assert state.last_label == expected_label
    assert state.frame_idx == 1
    assert state.last_event == "HOLD"


@pytest.mark.parametrize(
    "button_id",
    [ButtonId.A, ButtonId.B, ButtonId.X, ButtonId.Y],
)
def test_button_release(button_id):
    state = AppState()
    event = ButtonEvent(button_id, ButtonEventKind.RELEASE)
    state.update([event])

    assert state.counter == 0
    assert state.frame_idx == 1
    assert state.last_label == "-"

def test_report():
    state = AppState(frame_idx=3, counter=42, last_label="X")
    assert state.report() == "frame: 3, counter: 42, last pressed: X, last event: -"

def test_reset():
    state = AppState()
    state.update([ButtonEvent(ButtonId.A, ButtonEventKind.PRESS), ButtonEvent(ButtonId.B, ButtonEventKind.PRESS),
                  ButtonEvent(ButtonId.X, ButtonEventKind.PRESS), ButtonEvent(ButtonId.Y, ButtonEventKind.PRESS)])

    state.reset()

    assert state.frame_idx == 0
    assert state.counter == 0
    assert state.last_label == "-"

def test_update_with_empty_events():
    state = AppState()

    # No events
    state.update([])

    assert state.frame_idx == 1
    assert state.counter == 0
    assert state.last_label == "-"

    # Press A
    state.update([ButtonEvent(ButtonId.A, ButtonEventKind.PRESS)])

    assert state.frame_idx == 2
    assert state.counter == -1
    assert state.last_label == "A"

def test_multiple_events():
    state = AppState()

    state.update([ButtonEvent(ButtonId.A, ButtonEventKind.PRESS), ButtonEvent(ButtonId.A, ButtonEventKind.HOLD), ButtonEvent(ButtonId.B, ButtonEventKind.PRESS)])

    assert state.frame_idx == 1
    assert state.counter == -2   # A (press) = -1 & A (hold) = 1 & B (press) = -2 -> 2
    assert state.last_label == "B"
