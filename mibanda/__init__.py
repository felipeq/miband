# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
# This software is under the terms of GPLv3 or later.

from datetime import datetime

from gattlib import GATTRequester

# just make it available for other modules
from services import DiscoveryService
DiscoveryService


UUID_DEVICE_NAME = "0000ff02-0000-1000-8000-00805f9b34fb"
UUID_BATTERY     = "0000ff0c-0000-1000-8000-00805f9b34fb"
UUID_STEPS       = "0000ff06-0000-1000-8000-00805f9b34fb"
UUID_LE_PARAMS   = "0000ff09-0000-1000-8000-00805f9b34fb"


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


class BandDevice(object):
    def __init__(self, address):
        self.address = address
        self.requester = GATTRequester(address)

    def getAddress(self):
        return self.address

    def getName(self):
        data = self.requester.read_by_uuid(UUID_DEVICE_NAME)
        return data[0]

    def getBatteryInfo(self):
        data = self.requester.read_by_uuid(UUID_BATTERY)
        return BatteryInfo(data[0])

    def getSteps(self):
        data = self.requester.read_by_uuid(UUID_STEPS)[0]
        return ord(data[0]) + (ord(data[1]) << 8)
        
    def getLEParams(self):
        data = self.requester.read_by_uuid(UUID_LE_PARAMS)[0]
        return LEParams(data)
        

# NOTE: call this only once!
from services import IOService
IOService().start()
