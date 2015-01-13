#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import os
import wise
from subprocess import Popen
from peewee import SqliteDatabase, Model, CharField, BooleanField, IntegerField
import mibanda

home = os.environ.get("HOME")
db_path = os.path.join(home, "./config/migui.db")
db = SqliteDatabase(db_path)


class UserProfile(Model):
    male = BooleanField()
    age = IntegerField()
    height = IntegerField()
    weight = IntegerField()

    class Meta:
        database = db


class DeviceProfile(Model):
    device_address = CharField()
    uid = IntegerField()

    class Meta:
        database = db


class DeviceManager(object):
    def discover(self, timeout, current):
        ds = mibanda.DiscoveryService()
        bands = ds.discover(timeout)

        retval = []
        for b in bands:
            retval.append({'address': b.getAddress(), 'name': b.getName()})
        return retval

    def connect(self, address, current):
        self.device = mibanda.BandDevice(address, "")
        self.device.connect()
        self.device.pair()

        u, d = self.get_profiles(address)
        self.device.setUserInfo(d.uid, u.male, u.age, u.height, u.weight, 0)

    def get_profiles(self, address):
        user = UserProfile.select()[0]
        device = DeviceProfile(DeviceProfile.address == address)
        return user, device


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
