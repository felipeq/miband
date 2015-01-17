# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
# This software is under the terms of GPLv3 or later.

import time
from datetime import datetime
import struct
import gattlib


UUID_DEVICE_INFO   = "0000ff01-0000-1000-8000-00805f9b34fb"
UUID_DEVICE_NAME   = "0000ff02-0000-1000-8000-00805f9b34fb"
UUID_USER_INFO     = "0000ff04-0000-1000-8000-00805f9b34fb"
UUID_CONTROL_POINT = "0000ff05-0000-1000-8000-00805f9b34fb"
UUID_STEPS         = "0000ff06-0000-1000-8000-00805f9b34fb"
UUID_LE_PARAMS     = "0000ff09-0000-1000-8000-00805f9b34fb"
UUID_DATE_TIME     = "0000ff0a-0000-1000-8000-00805f9b34fb"
UUID_BATTERY       = "0000ff0c-0000-1000-8000-00805f9b34fb"

HANDLE_DATE_TIME     = 0x27
HANDLE_USER_INFO     = 0x19
HANDLE_CONTROL_POINT = 0x1b
HANDLE_TEST          = 0x2e
HANDLE_PAIR          = 0x33


def h2s(src):
    """ hex to string: '02:1b' -> '\x02\x1b' """
    data = map(lambda x: int(x, 16), src.split(":"))
    return str(bytearray(data))


class Colors(object):
    BLACK   = (0, 0, 0)
    BLUE    = (0, 0, 6)
    GREEN   = (0, 6, 0)
    AQUA    = (0, 6, 6)
    RED     = (6, 0, 0)
    FUCHSIA = (6, 0, 6)
    YELLOW  = (6, 6, 0)
    GRAY    = (3, 3, 3)
    WHITE   = (6, 6, 6)
    ORANGE  = (6, 3, 0)


class BatteryInfo(object):
    def __init__(self, data):
        fields = map(ord, data)
        self.level = fields[0]
        self.last_charged = datetime(
            fields[1] + 2000,
            fields[2] + 1,
            *fields[3:6])
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

    def setDateTime(self, dt=None):
        if dt is None:
            dt = datetime.now()

        data = [(dt.year - 2000) & 0xff, dt.month - 1, dt.day,
                dt.hour, dt.minute, dt.second]

        self.requester.write_by_handle(HANDLE_DATE_TIME, str(bytearray(data)))

    def getDateTime(self):
        start = datetime.now()
        self.setDateTime(start)

        c = 4
        try:
            data = self.requester.read_by_uuid(UUID_DATE_TIME)[0]
        except RuntimeError:
            c -= 1
            if not c:
                raise
            time.sleep(.2)

        fields = map(ord, data)[6:]
        device_dt = datetime(fields[0] + 2000, fields[1] + 1, *fields[2:])
        elapsed = datetime.now() - start
        self.setDateTime(device_dt + elapsed)

        return device_dt

    def selfTest(self):
        self.requester.write_by_handle(HANDLE_TEST, str(bytearray([2])))

    def pair(self):
        self.requester.write_by_handle(HANDLE_PAIR, str(bytearray([2])))

        counter = 5
        while counter:
            time.sleep(0.1)
            try:
                data = self.requester.read_by_handle(HANDLE_PAIR)[0]
            except RuntimeError:
                continue

            if ord(data[0]) == 0x2:
                break
            counter -= 1

    def setUserInfo(self, uid, male, age, height, weight, type_, alias=None):
        seq = bytearray(20)

        seq[:4] = [ord(i) for i in struct.pack("<I", uid)]
        seq[4] = bool(male)
        seq[5] = age & 0xff
        seq[6] = height & 0xff
        seq[7] = weight & 0xff
        seq[8] = type_ & 0xff

        if alias is None:
            alias = str(uid)
            alias = "0" * (10 - len(alias)) + alias

        assert len(alias) == 10, "'alias' size must be 10 chars"
        seq[9:19] = alias

        addr = self.getAddress()
        crc = self._getCRC8(seq[:19])
        crc = (crc ^ int(addr[-2:], 16)) & 0xff
        seq[19] = crc

        self.requester.write_by_handle(HANDLE_USER_INFO, str(seq))

    def flashLeds(self, r, g, b):
        """ levels range from 1 (min bright) to 6 (max bright) """
        self.requester.write_by_handle(
            HANDLE_CONTROL_POINT, str(bytearray([0x0e, r, g, b, 0x01])))

    def startVibration(self):
        """ this will put the band in vibration mode up to 10 seconds,
        or until you tap the band """
        self.requester.write_by_handle(HANDLE_CONTROL_POINT, h2s("8:1"))

    def stopVibration(self):
        """ will stop the vibration mode, if running """
        self.requester.write_by_handle(HANDLE_CONTROL_POINT, h2s("13"))

    def locate(self):
        self.requester.write_by_handle(
            HANDLE_CONTROL_POINT, str(bytearray([0x08, 0x00])))

    def _getCRC8(self, data):
        crc = 0
        for i in range(0, len(data)):
            crc = crc ^ (data[i] & 0xff)

            for j in range(8):
                if crc & 0x01:
                    crc = (crc >> 1) ^ 0x8c
                else:
                    crc >>= 1
        return crc


class DiscoveryService(object):
    def __init__(self, device="hci0"):
        self.service = gattlib.DiscoveryService(device)

    def discover(self, timeout=3):
        bands = []
        for addr, name in self.service.discover(timeout).items():
            band = BandDevice(addr, name)
            bands.append(band)
        return bands
