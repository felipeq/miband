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

    # data = req.read_by_uuid("0000ff0e-0000-1000-8000-00805f9b34fb")
    # data = req.read_by_uuid("0000ff07-0000-1000-8000-00805f9b34fb")
    data = req.read_by_handle(0x29)
    # data = req.write_by_handle(0x1b, str(bytearray([9])))

    print len(data), len(data[0])
    hexdump(data[0])

    print "OK"


