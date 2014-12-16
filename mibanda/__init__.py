# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
# This software is under the terms of GPLv3 or later.

from services import DiscoveryService
from devices import BandDevice

# NOTE: call this only once!
from services import IOService
IOService().start()
