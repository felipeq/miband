#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import os
import wise
from subprocess import Popen
import mibanda


class DeviceManager(object):
    def discover(self, timeout, current):
        ds = mibanda.DiscoveryService()
        bands = ds.discover(timeout)

        retval = []
        for b in bands:
            retval.append({'address': b.getAddress(), 'name': b.getName()})
        return retval

    def connect(self, addr, current):
        print "connect to {} called".format(addr)


class Backend(object):
    def __init__(self):
        broker = wise.initialize(port=7154, properties={"TornadoApp.debug": True})
        static = os.path.join(wise.dirname(__file__), "static")
        broker.register_StaticFS('/static', static)
        url = broker.get_url('static/index.html')

        adapter = broker.createObjectAdapter("Adapter", "-w ws")
        adapter.add(DeviceManager(), "DeviceManager")

        cmd = ("google-chrome "
               "--disable-translate "
               "--disable-popup-blocking "
               "--user-data-dir=/tmp/ "
               "--disable-session-crashed-bubble "
               "--no-first-run "
               "--window-size=500,600 "
               "--app={}".format(url))

        browser = Popen(cmd.split())

        broker.waitForShutdown()
        browser.wait()


if __name__ == "__main__":
    Backend()
