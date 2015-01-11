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

    gender = 1    # male
    age = 30      # years
    height = 189  # cms
    weight = 80   # kgs

    type_ = 01
    uid = 1553037356
    alias = str(uid)  # must be 10 digits

    dev.setUserInfo(uid, gender, age, height, weight, type_, alias)

    time.sleep(10)
    print "OK"
