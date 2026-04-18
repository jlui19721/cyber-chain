# @file tests/test_render.py
# @brief Focus on testing the `render` function
from app.render import render
from app.state import AppState

def test_render_dimensions_and_mode():
    state = AppState(frame_idx=3, counter=12, last_label="B")
    img = render(state)

    assert img.width == 240
    assert img.height == 240
    assert img.mode == "RGB"

def test_render_dimensions():
    state = AppState(frame_idx=3, counter=12, last_label="B")
    img = render(state, w=320, h=160)

    assert img.width == 320
    assert img.height == 160
