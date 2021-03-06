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
    time.sleep(1)

    print "Enabling RealTime notifications..."
    dev.enableRealTimeSteps()

    print "Now, move on! (Ctrl+c to stop)"
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        dev.disableRealTimeSteps()

    print "OK"
