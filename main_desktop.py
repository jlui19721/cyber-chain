import signal
import time
import threading
from app.helloworld.helloworldapp import HelloWorldApp

"""Desktop Implementation"""
from hardware.desktop_pygame import make_desktop

def main():
    stop = threading.Event()
    display, buttons, audio = make_desktop(stop_event=stop)
    app = HelloWorldApp(display, buttons, audio, quit_event=stop)

    try:
        app.run()
    finally:
        app.shutdown()
        audio.shutdown()
        display.shutdown()
        buttons.shutdown()

if __name__ == "__main__":
    main()
