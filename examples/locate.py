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

    print "Sending locate...",
    dev.locate()

    time.sleep(2)
    print "OK"
