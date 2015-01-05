#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys

from gattlib import GATTRequester
from hexdump import hexdump


def wr(req, info):
    fields = info.split()
    handle = int(fields[0], 16)
    data = map(lambda x: int(x, 16), fields[1:])

    print "write, handle: {}, data: {}".format(handle, fields[1:])
    print req.write_by_handle(handle, str(bytearray(data)))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {} <mac_address>".format(sys.argv[0])
        sys.exit(1)

    req = GATTRequester(sys.argv[1])

    # print req.write_by_handle(
    #     0x1b, str(bytearray([0x0e, 0x04, 0x05, 0x00, 0x01])))

    # data = req.read_by_uuid("0000ff0e-0000-1000-8000-00805f9b34fb")
    # data = req.read_by_uuid("0000ff07-0000-1000-8000-00805f9b34fb")
    # data = req.read_by_handle(0x29)
    # data = req.write_by_handle(0x1b, str(bytearray([9])))

    # print len(data), len(data[0])
    # hexdump(data[0])

    # wr(req, "17 01 00")
    # wr(req, "1e 01 00")
    # wr(req, "21 01 00")
    # wr(req, "2c 01 00")
    # wr(req, "31 01 00")

    wr(req, "19 2c 78 91 5c 01 2c ae 5d 01 31 35 "
       "35 33 30 33 37 33 35 36 0f")

    import time
    time.sleep(20)

    req.write_by_handle(
        0x1b, str(bytearray([0x0e, 0x04, 0x05, 0x00, 0x01])))


    print "OK"
