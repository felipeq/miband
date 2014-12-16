#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

import sys
from datetime import datetime
from mibanda import BandDevice

if len(sys.argv) < 3:
    print "USAGE: {} <addr> <name>".format(sys.argv[0])
    sys.exit(1)

b = BandDevice(sys.argv[1], sys.argv[2])

print "NAME:", b.getName()
print "ADDRESS:", b.getAddress()

binfo = b.getBatteryInfo()
last_charged = datetime(
    binfo.last_charged.year,
    binfo.last_charged.month,
    binfo.last_charged.day,
    binfo.last_charged.hour,
    binfo.last_charged.minute,
    binfo.last_charged.second)

print "BATTERY:"
print " - level:", binfo.level
print " - last_charged:", last_charged
print " - charge_counter:", binfo.charge_counter
print " - status:", binfo.status
