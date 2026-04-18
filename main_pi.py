import signal
import time
import threading

from app.helloworldapp import HelloWorldApp
from hardware import display_pirate, buttons_pirate

"""Raspberry Pi Implementation"""

def main():
    print("Booting up...")
    display = None
    buttons = None
    app = None
    worker = None
    stop = threading.Event()  # Event to signal the main thread to stop

    def request_stop(signum=None, frame=None):
        stop.set()

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)

    try:
        display = display_pirate.make_pirate_display()
        buttons = buttons_pirate.make_pirate_buttons()
        time.sleep(2)  # Wait 2 seconds to confirm boot up
        print("Components initialized...")

        app = HelloWorldApp(display, buttons, quit_event=stop)
        worker = threading.Thread(target=app.run, name="HelloWorldApp", daemon=False)
        worker.start()

        stop.wait()

    finally:
        if app is not None:
            app.shutdown()
        if worker is not None:
            worker.join(timeout=5.0)

        print("Shutting down...")
        if display is not None:
            display.shutdown()
        if buttons is not None:
            buttons.shutdown()

if __name__ == "__main__":
    main()
