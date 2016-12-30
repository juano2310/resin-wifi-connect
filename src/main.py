#!/usr/bin/env python

import time
from sense_hat import SenseHat
import subprocess
import process


def main():
    while True:
        # Run one process loop
        process.main()

        # Sleep to avoid 100% CPU usage
        time.sleep(5)


@touch.on(touch.BUTTON)
def handle_button(ch, evt):
    # When the button is pressed resin-wifi-connect is started with `--clear'
    # flag set to 'true'. This forces resin-wifi-connect to remove any
    # previously configured WiFi connections.
    print("Button pressed")
    subprocess.call(["node", "resin-wifi-connect/src/app.js", "--clear=true"])


if __name__ == "__main__":
    main()
