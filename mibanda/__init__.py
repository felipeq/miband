# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
# This software is under the terms of GPLv3 or later.

from datetime import datetime
import gattlib


UUID_DEVICE_INFO = "0000ff01-0000-1000-8000-00805f9b34fb"
UUID_DEVICE_NAME = "0000ff02-0000-1000-8000-00805f9b34fb"
UUID_STEPS       = "0000ff06-0000-1000-8000-00805f9b34fb"
UUID_LE_PARAMS   = "0000ff09-0000-1000-8000-00805f9b34fb"
UUID_BATTERY     = "0000ff0c-0000-1000-8000-00805f9b34fb"

HANDLE_TEST          = 0x2e
HANDLE_USER_INFO     = 0x19
HANDLE_CONTROL_POINT = 0x1b


class BatteryInfo(object):
    def __init__(self, data):
        fields = map(ord, data)
        self.level = fields[0]
        self.last_charged = datetime(2000 + fields[1], *fields[2:6])
        self.charge_counter = fields[7] + (fields[8] << 8)

        status_names = {1: 'low', 2: 'medium', 3: 'full', 4: 'not charging'}
        self.status = status_names.get(fields[9], "unknown")


class LEParams(object):
    def __init__(self, data):
        fields = map(ord, data)
        self.minimum_connection_interval = fields[0] + (fields[1] << 8)
        self.maximum_connection_interval = fields[2] + (fields[3] << 8)
        self.latency = fields[4] + (fields[5] << 8)
        self.timeout = fields[6] + (fields[7] << 8)
        self.connection_interval = fields[8] + (fields[9] << 8)
        self.advertisement_interval = fields[10] + (fields[11] << 8)


class DeviceInfo(object):
    def __init__(self, data):
        fields = map(ord, data)
        self.firmware_version = "{}.{}.{}.{}".format(*reversed(fields[-4:]))


class BandDevice(object):
    def __init__(self, address, name):
        self.address = address
        self.name = name

        self.requester = gattlib.GATTRequester(address, False)

    def connect(self):
        self.requester.connect(True)

    def getAddress(self):
        return self.address

    def getName(self, cached=True):
        if cached:
            return self.name

        data = self.requester.read_by_uuid(UUID_DEVICE_NAME)
        return data[0]

    def getBatteryInfo(self):
        data = self.requester.read_by_uuid(UUID_BATTERY)
        return BatteryInfo(data[0])

    def getDeviceInfo(self):
        data = self.requester.read_by_uuid(UUID_DEVICE_INFO)[0]
        return DeviceInfo(data)

    def getSteps(self):
        data = self.requester.read_by_uuid(UUID_STEPS)[0]
        return ord(data[0]) + (ord(data[1]) << 8)

    def getLEParams(self):
        data = self.requester.read_by_uuid(UUID_LE_PARAMS)[0]
        return LEParams(data)

    def selfTest(self):
        self.requester.write_by_handle(HANDLE_TEST, str(bytearray([2])))

    def pair(self):
        data = [0x2c, 0x78, 0x91, 0x5c, 0x01, 0x2c, 0xae, 0x5d,
                0x01, 0x31, 0x35, 0x35, 0x33, 0x30, 0x33, 0x37,
                0x33, 0x35, 0x36, 0x0f]
        self.requester.write_by_handle(
            HANDLE_USER_INFO, str(bytearray(data)))

    def flashLeds(self, r, g, b):
        """ levels range from 1 (min bright) to 6 (max bright) """
        self.requester.write_by_handle(
            HANDLE_CONTROL_POINT, str(bytearray([0x0e, r, g, b, 0x01])))

    def locate(self):
        self.requester.write_by_handle(
            HANDLE_CONTROL_POINT, str(bytearray([0x08, 0x00])))


class DiscoveryService(object):
    def __init__(self, device="hci0"):
        self.service = gattlib.DiscoveryService(device)

    def discover(self, timeout=3):
        bands = []
        for addr, name in self.service.discover(timeout).items():
            band = BandDevice(addr, name)
            bands.append(band)
        return bands
