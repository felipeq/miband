#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys
import time
from datetime import datetime, timedelta

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

    print "-" * 60
    from mibanda import HANDLE_CONTROL_POINT, h2s
    req = dev.requester

    dt = dev.getDateTime()
    wait = timedelta(seconds=90)

    to = dt + wait
    seq = "4:0:1:f:0:11:{:x}:{:x}:0:0:0".format(to.hour, to.minute)
    print "4:0:1:f:0:11:{:x}:{:x}:0:0:0".format(to.hour, to.minute)
    # req.write_by_handle(HANDLE_CONTROL_POINT, h2s(seq))

    print "OK"
