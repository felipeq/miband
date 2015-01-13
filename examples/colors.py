#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys
import time

from mibanda import BandDevice


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {} <mac_address>".format(sys.argv[0])
        sys.exit(1)

    print "Connectiing, please wait..."
    dev = BandDevice(sys.argv[1], "")
    dev.connect()

    print "Pairing..."
    dev.pair()

    # NOTE: after locate, you must send the user info to your miband
    dev.setUserInfo(uid=1, male=False, age=2, height=2, weight=2, type_=0)
    time.sleep(5)

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
        dev.flashLeds(r, g, b)
        time.sleep(2)

    print "OK"
