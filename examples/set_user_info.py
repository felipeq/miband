#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys
import time
import struct

from mibanda import BandDevice


def getCRC8(data):
    crc = 0
    for i in range(0, len(data)):
        crc = crc ^ (data[i] & 0xff)

        for j in range(8):
            if crc & 0x01:
                crc = (crc >> 1) ^ 0x8c
            else:
                crc >>= 1
    return crc


def set_user_info(dev, uid, gender, age, height, weight, type_, alias):
    seq = bytearray(20)

    seq[:4] = [ord(i) for i in struct.pack("<I", uid)]
    seq[4] = bool(gender)
    seq[5] = age & 0xff
    seq[6] = height & 0xff
    seq[7] = weight & 0xff
    seq[8] = type_ & 0xff

    assert len(alias) == 10, "Alias size must be 10"
    seq[9:19] = alias

    addr = dev.getAddress()

    crc = getCRC8(seq[:19])
    crc = (crc ^ int(addr[-2:], 16)) & 0xff

    seq[19] = crc
    dev.requester.write_by_handle(0x19, str(seq))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {} <mac_address>".format(sys.argv[0])
        sys.exit(1)

    dev = BandDevice(sys.argv[1], "")
    dev.connect()
    expect = "2c:78:91:5c:01:2c:ae:5d:01:31:35:35:33:30:33:37:33:35:36:0f"

    uid = struct.unpack("<I", "\x2c\x78\x91\x5c")[0]
    gender = 1    # male
    age = 30      # years
    height = 189  # cms
    weight = 80   # kgs
    type_ = 01
    alias = "1553037356"

    set_user_info(dev, uid, gender, age, height, weight, type_, alias)

    time.sleep(5)
    print "OK"
