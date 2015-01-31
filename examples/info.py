#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

from __future__ import print_function

import sys
from datetime import datetime
from mibanda import BandDevice


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <mac_address>".format(sys.argv[0]))
        sys.exit(1)

    print("Connectiing, please wait...")
    dev = BandDevice(sys.argv[1], "")
    dev.connect()

    binfo = dev.getBatteryInfo()
    elapsed = (datetime.now() - binfo.last_charged).days
    print("BATTERY:")
    print(" - level: {}%".format(binfo.level))
    print(" - last_charged:", binfo.last_charged)
    print(" - charge_counter: {} times".format(binfo.charge_counter))
    print(" - elapsed: {} days".format(elapsed))
    print(" - status:", binfo.status)

    print("MAC:", dev.getAddress())
    print("NAME:", dev.getName(cached=False))
    print("STEPS:", dev.getSteps())

    params = dev.getLEParams()
    print("LE PARAMS:")
    print(" - minimum_connection_interval:", params.minimum_connection_interval)
    print(" - maximum_connection_interval:", params.maximum_connection_interval)
    print(" - latency:", params.latency)
    print(" - timeout:", params.timeout)
    print(" - connection_interval:", params.connection_interval)
    print(" - advertisement_interval:", params.advertisement_interval)

    devinfo = dev.getDeviceInfo()
    print("DEVICE INFO:")
    print(" - firmware_version: ", devinfo.firmware_version)
