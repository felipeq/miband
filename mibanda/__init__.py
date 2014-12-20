# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
# This software is under the terms of GPLv3 or later.

from datetime import datetime

from gattlib import GATTRequester

# just make it available for other modules
from services import DiscoveryService
DiscoveryService


HANDLER_BATTERY = 0x2b


class BatteryInfo(object):
    def __init__(self, data):
        fields = map(ord, data)
        self.level = fields[0]
        self.last_charged = datetime(2000 + fields[1], *fields[2:6])
        self.charge_counter = fields[7] + (fields[8] << 8)

        status_names = {1: 'low', 2: 'medium', 3: 'full', 4: 'not charging'}
        self.status = status_names.get(fields[9], "unknown")


class BandDevice(object):
    def __init__(self, address):
        self.address = address
        self.requester = GATTRequester(address)

    def getBatteryInfo(self):
        data = self.requester.read_by_handle(HANDLER_BATTERY)
        return BatteryInfo(data)


# NOTE: call this only once!
from services import IOService
IOService().start()
