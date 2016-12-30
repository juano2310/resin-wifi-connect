#!/usr/bin/env python

import subprocess
from sense_hat import SenseHat

sense = SenseHat()

def main():
    # Get the current SSID
    SSID = None
    try:
        SSID = subprocess.check_output(["iwgetid", "-r"]).strip()
    except subprocess.CalledProcessError:
        # If there is no connection subprocess throws a 'CalledProcessError'
        pass

    # Show status on the LCD display
    if SSID is None:
        sense.show_message("Not connected")
    else:
        sense.show_message("SSID: " + SSID)


if __name__ == "__main__":
    main()
