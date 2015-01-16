#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys
import time
from hexdump import hexdump

from mibanda import BandDevice, HANDLE_DATE_TIME


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
    time.sleep(2)

    print "Sending notify..."

    req = dev.requester
    data = [0x0e, 0x00, 0x0f, 0x11, 0x2c, 0x32,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff]

    hexdump("".join(map(chr, data)))
    req.write_by_handle(HANDLE_DATE_TIME, str(bytearray(data)))
    recv = req.read_by_handle(HANDLE_DATE_TIME)
    hexdump("".join(recv))

    # # middle led blue (2 secs), 10 vibrations (stops if tap)
    # dev.requester.write_by_handle(HANDLE_CONTROL_POINT, str(bytearray([8, 1])))

    time.sleep(2)
    print "OK"
