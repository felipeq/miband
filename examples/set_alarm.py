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
    time.sleep(1)

    print "-" * 60
    from mibanda import HANDLE_CONTROL_POINT, h2s
    req = dev.requester

    now = datetime.now()
    dev.setDateTime(now)

    wait = timedelta(seconds=60)
    to = now + wait

    seq = [
        0x04,        # 01: set_alarm opcode
        0x00,        # 02: alarm number (first)
        0x01,        # 03: enabled (true)
        0x0f,        # 04: ?
        0x00,        # 05: ?
        0x11,        # 06: repeat (no, only once)
        to.hour,     # 07: hour
        to.minute,   # 08: minute
        0x00,        # 09: ? (seconds?)
        0x00,        # 10: intelligent (no)
        0x00,        # 11: repeat pattern (no repeat)
    ]

    print now
    print to

    req.write_by_handle(HANDLE_CONTROL_POINT, h2s(seq))

    time.sleep(2)
    print "OK"
