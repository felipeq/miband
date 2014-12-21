#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys

from mibanda.gattlib import GATTRequester
from hexdump import hexdump


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {} <mac_address>".format(sys.argv[0])
        sys.exit(1)

    req = GATTRequester(sys.argv[1])
    data = req.write_by_handle(0x2e, str(bytearray([2])))    
    print "OK"
