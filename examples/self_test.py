#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys

# from mibanda import BandDevice
from mibanda.gattlib import GATTRequester
from hexdump import hexdump


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {} <mac_address>".format(sys.argv[0])
        sys.exit(1)

    # dev = BandDevice(sys.argv[1])
    # print dev

    req = GATTRequester(sys.argv[1])

    # paired = req.read_by_handle(0x32)[0]
    # print map(ord, paired)

    # data = map(ord, "OSCAR")
    # print "write data:", data
    # req.write_by_handle(0x14, str(bytearray(data)))

    # req.write_by_handle(, str(bytearray(data)))
    
    # for i in range(1, 75):
    #     try:
    #         sys.stdout.write(hex(i) + " ")
    #         items = req.read_by_handle(i)
    #         hexdump(items[0])
    #     except RuntimeError:
    #         print "invalid handle:", i

    items = req.read_by_handle(0x27)[0]
    print len(items)
    hexdump(items)


    print "OK"
