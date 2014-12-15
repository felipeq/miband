#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

import sys
from mibanda import BandDevice

if len(sys.argv) < 3:
    print "USAGE: {} <addr> <name>".format(sys.argv[0])
    sys.exit(1)

b = BandDevice(sys.argv[1], sys.argv[2])

print "NAME:", b.getName()
print "ADDRESS:", b.getAddress()

binfo = b.getBatteryInfo()
print "BATTERY:"
print " - level:", binfo.level
print " - last_charged:", binfo.last_charged
print " - charge_counter:", binfo.charge_counter
print " - status:", binfo.charge_counter
