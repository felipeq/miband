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

    male = True   # gender
    age = 30      # years
    height = 189  # cms
    weight = 80   # kgs

    type_ = 00
    uid = 1563037356
    alias = str(uid)  # must be 10 digits

    print "Setting user info..."
    dev.setUserInfo(uid, male, age, height, weight, type_)

    time.sleep(1)
    dev.locate()

    time.sleep(10)
    print "OK"
