#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

import sys
from mibanda import DiscoveryService


ds = DiscoveryService("hci0", 2)
bands = ds.discover()

if not bands:
    print "No bands found!"
    sys.exit(-1)

for band in bands:
    print "Band found, called '{}', addres: {}".format(
        band.getName(), band.getAddress())

print "OK"
