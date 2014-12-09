# -*- mode: python; coding: utf-8 -*-

import os
from commodity.os_ import SubProcess


class BandDevice(object):
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr

    def __repr__(self):
        return "<BandDevice, addr: {}, name: {}".format(
            self.addr, self.name)


class DiscoveryService(object):
    def discover(self, timeout=3):
        output = self.get_discover_results(timeout)
        devices = self.get_unique_devices(output)
        return self.create_band_objects(devices)

    def get_discover_results(self, timeout):
        pwd = os.path.abspath(os.path.dirname(__file__))
        cmd = os.path.join(pwd, "lescan.sh")

        p = SubProcess(
            "{0} {1}".format(cmd, timeout),
            shell=True)
        p.wait()

        return p.stdout.read()

    def get_unique_devices(self, output):
        retval = {}

        for line in output.splitlines():
            addr = line[:17]
            name = line[17:].strip()
            if name == "(unknown)":
                name = None
            retval[addr] = name or retval.get(addr)

        return retval

    def create_band_objects(self, devices):
        retval = []
        for addr, name in devices.items():
            retval.append(BandDevice(name, addr))
        return retval
