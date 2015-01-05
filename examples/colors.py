#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys
import time

from mibanda import BandDevice


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {} <mac_address>".format(sys.argv[0])
        sys.exit(1)

    dev = BandDevice(sys.argv[1], "")
    dev.connect()
    dev.pair()

    time.sleep(10)

    print "changing colors..."
    colors = [(0, 0, 0),  # off
              (0, 0, 6),  # blue
              (0, 6, 0),  # green
              (0, 6, 6),  # cyan
              (6, 0, 0),  # red
              (6, 0, 6),  # magenta
              (6, 6, 0),  # yellow
              (6, 6, 6)]  # white

    for r, g, b in colors:
        dev.flash_leds(r, g, b)
        time.sleep(2)

    print "OK"
