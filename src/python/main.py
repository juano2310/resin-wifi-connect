#!/usr/bin/env python

import time
from sense_hat import SenseHat
import subprocess
import process

sense = SenseHat()
sense.clear()  # Blank the LED matrix

def main():
    while True:
        # Run one process loop
        process.main()

        # Sleep to avoid 100% CPU usage
        time.sleep(5)

def handle_button(ch, evt):
    # When the button is pressed resin-wifi-connect is started with `--clear'
    # flag set to 'true'. This forces resin-wifi-connect to remove any
    # previously configured WiFi connections.
    print("Button pressed")
    subprocess.call(["node", "src/app.js", "--clear=true"])


if __name__ == "__main__":
    main()
