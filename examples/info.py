#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys

from mibanda import BandDevice


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {} <mac_address>".format(sys.argv[0])
        sys.exit(1)

    dev = BandDevice(sys.argv[1])

    print "Connectiing, please wait..."
    binfo = dev.getBatteryInfo()

    print "BATTERY:"
    print " - level:", binfo.level
    print " - last_charged:", binfo.last_charged
    print " - charge_counter:", binfo.charge_counter
    print " - status:", binfo.status

    print "MAC:", dev.getAddress()
    print "NAME:", dev.getName()
