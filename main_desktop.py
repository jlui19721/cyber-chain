import signal
import time
import threading
from app.helloworldapp import HelloWorldApp

"""Desktop Implementation"""
from hardware.desktop_pygame import make_desktop

def main():
    stop = threading.Event()
    display, buttons = make_desktop(stop_event=stop)
    app = HelloWorldApp(display, buttons, quit_event=stop)

    try:
        app.run()
    finally:
        app.shutdown()
        display.shutdown()
        buttons.shutdown()

if __name__ == "__main__":
    main()
