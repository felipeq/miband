#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

import sys
from mibanda import DiscoveryService


timeout = 5

print "Starting discover for {} seconds...".format(timeout)
ds = DiscoveryService()
bands = ds.discover(timeout)

if not bands:
    print "No bands found!"
    sys.exit(-1)

for band in bands:
    print "Band found, called '{}', addres: {}".format(
        band.getName(), band.getAddress())

print "Done."
