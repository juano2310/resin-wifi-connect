#!/usr/bin/env python

import subprocess
from sense_hat import SenseHat

sense = SenseHat()
sense.set_rotation(90)

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
        sense.show_message("Not connected", text_colour=[255, 0, 0])
    else:
        sense.show_message("Connected", text_colour=[0, 255, 0]))

if __name__ == "__main__":
    main()
