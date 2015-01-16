#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

import sys
from mibanda import DiscoveryService


ds = DiscoveryService()
bands = ds.discover(5)

if not bands:
    print "No bands found!"
    sys.exit(-1)

for band in bands:
    print "Band found, called '{}', addres: {}".format(
        band.getName(), band.getAddress())

print "Done."
