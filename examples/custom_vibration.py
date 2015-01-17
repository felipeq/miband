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

    print "Faster vibration (10 times)..."
    time.sleep(2)
    dev.customVibration(10, 25, 10)

    print "Water drop vibration (5 times)..."
    time.sleep(2)
    dev.customVibration(5, 25, 1200)

    print "Longer vibrations, no 'off time' (5 times)..."
    time.sleep(2)
    dev.customVibration(5, 500, 0)

    print "OK"
