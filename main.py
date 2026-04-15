import time

FRAME_SECONDS = 1.0 / 30.0  # ~30 FPS; tune for Pi Zero vs Pi 4

def main():
    display = make_display()
    buttons = make_input()
    state = AppState()  # emoji index, animation phase, etc.

    display.clear()
    last = time.monotonic()

    while True:
        now = time.monotonic()
        dt = now - last
        last = now

        events = buttons.poll()  # e.g. list of ButtonEven objects
        state.update(dt, events)  # pure app logic; no GPIO here

        frame = state.render_frame()   # PIL Image or buffer your display expects
        display.show(frame)

        # Fixed timestep: sleep remainder of frame
        elapsed = time.monotonic() - now
        sleep_for = FRAME_SECONDS - elapsed
        if sleep_for > 0:
            time.sleep(sleep_for)
