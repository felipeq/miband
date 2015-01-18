#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys
import time
from datetime import datetime, timedelta

from mibanda import BandDevice, EVERYDAY


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

    print "Setting alarm to run in a few seconds..."
    timeout = 90
    now = datetime.now()
    dev.setDateTime()
    when = now + timedelta(seconds=timeout)
    dev.setAlarm1(when, smart=False, repeat=EVERYDAY)

    time.sleep(1)
    print "OK"
