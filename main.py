import time

from hardware import display_pirate, buttons_pirate

FRAME_SECONDS = 1.0 / 30.0  # ~30 FPS; tune for Pi Zero vs Pi 4

def main():
    print("Booting up...")
    frame_num = 0
    display = None
    buttons = None

    try:
        display = display_pirate.make_pirate_display()
        buttons = buttons_pirate.make_pirate_buttons()
        time.sleep(2)  # Wait 2 seconds to confirm boot up
        print("Components initialized...")
        #state = AppState()  # emoji index, animation phase, etc.

        display.clear()
        last = time.monotonic()

        while True:
            now = time.monotonic()
            dt = now - last
            last = now

            events = buttons.poll()  # e.g. list of ButtonEvent objects
            #state.update(dt, events)  # pure app logic; no GPIO here

            #frame = state.render_frame()   # PIL Image or buffer your display expects
            #display.show(frame)

            # Fixed timestep: sleep remainder of frame
            elapsed = time.monotonic() - now

            print(f"Frame {frame_num}\nElapsed: {elapsed:.6f}s\nEvents: {events}")
            frame_num += 1

            sleep_for = FRAME_SECONDS - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)
    finally:
        print("Shutting down...")
        if display is not None:
            display.shutdown()
        if buttons is not None:
            buttons.shutdown()

if __name__ == "__main__":
    main()
