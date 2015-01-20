# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
# This software is under the terms of GPLv3 or later.

import time
from datetime import datetime
import struct
import gattlib


class DiscoveryService(object):
    """Service to discover Mi Band devices over the air.

    ``device`` is the name of your Bluetooth hardware (could be get
    using ``hciconfig``). If not given, the first device is used:
    *hci0*. ::

      >>> sd = mibanda.DiscoveryService()

    .. note:: It may require superuser privileges (run as root, or using sudo).
    """

    def __init__(self, device="hci0"):
        self.service = gattlib.DiscoveryService(device)

    def discover(self, timeout=3):
        """ launch a LE scan to discover devices, up to 'timeout' seconds """
        bands = []
        for addr, name in self.service.discover(timeout).items():
            band = BandDevice(addr, name)
            bands.append(band)
        return bands


class BandDevice(object):
    """This is the main object of mibanda library. It represents a Mi
    Band device, and has those methods needed to read its state, and control/change
    its behaviour.

    ``address`` is its MAC address, in the form of a string like:
    ``00:11:22:33:44:55``. Name is the advertised Bluetooth name. It
    could be empty. ::

      >>> device = mibanda.BandDevice("88:0f:10:00:01:02", "MI")
    """

    def __init__(self, address, name=""):
        self.address = address
        self.name = name

        self.requester = gattlib.GATTRequester(address, False)

    def connect(self):
        """ connect to the Mi Band device
        """
        self.requester.connect(True)

    def getAddress(self):
        """ get device's MAC address """
        return self.address

    def getName(self, cached=True):
        """ get device's Bluetooth name """
        if cached:
            return self.name

        data = self.requester.read_by_uuid(UUID.DEVICE_NAME)
        return data[0]

    def getBatteryInfo(self):
        """ get information about device battery: level, status, charge counter,
        last charge, etc. """
        data = self.requester.read_by_uuid(UUID.BATTERY)
        return BatteryInfo(data[0])

    def getDeviceInfo(self):
        """ get device information: firmware version, etc. """
        data = self.requester.read_by_uuid(UUID.DEVICE_INFO)[0]
        return DeviceInfo(data)

    def getSteps(self):
        """ get current step counter value """
        data = self.requester.read_by_uuid(UUID.STEPS)[0]
        return ord(data[0]) + (ord(data[1]) << 8)

    def getLEParams(self):
        """ get Bluetooth LE (smart) connection parameters """
        data = self.requester.read_by_uuid(UUID.LE_PARAMS)[0]
        return LEParams(data)

    def setDateTime(self, dt=None):
        """ set device current date and time, 'dt' is a datetime.datetime object """
        if dt is None:
            dt = datetime.now()

        data = [(dt.year - 2000) & 0xff, dt.month - 1, dt.day,
                dt.hour, dt.minute, dt.second]

        self.requester.write_by_handle(Handle.DATE_TIME, str(bytearray(data)))

    def getDateTime(self):
        """ get device current date and time """

        # Note: reading directly will not get response from device, or
        # receives a malformed packet

        start = datetime.now()
        self.setDateTime(start)

        c = 4
        try:
            data = self.requester.read_by_uuid(UUID.DATE_TIME)[0]
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
        """ perform an internat test
        WARNING: this will erase status information on your device """
        self.requester.write_by_handle(Handle.TEST, str(bytearray([2])))

    def pair(self):
        """ pair device with this host """
        self.requester.write_by_handle(Handle.PAIR, str(bytearray([2])))

        counter = 5
        while counter:
            time.sleep(0.1)
            try:
                data = self.requester.read_by_handle(Handle.PAIR)[0]
            except RuntimeError:
                continue

            if ord(data[0]) == 0x2:
                break
            counter -= 1

    def setUserInfo(self, uid, male, age, height, weight, type_, alias=None):
        """ set user information on device: gender, age, height, weight, etc. """
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

        self.requester.write_by_handle(Handle.USER_INFO, str(seq))

    def flashLeds(self, r, g, b):
        """ toggle LEDs status, using values for red (r), green (g) and blue
        (b), levels range from 1 (min bright) to 6 (max bright) """
        self.requester.write_by_handle(
            Handle.CONTROL_POINT, str(bytearray([0x0e, r, g, b, 0x01])))

    def startVibration(self):
        """ put the band in vibration mode up to 10 seconds, or until you
        tap the band """
        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s("8:1"))

    def stopVibration(self):
        """ stop the vibration mode, if running """
        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s("13"))

    def customVibration(self, times, on_time, off_time):
        """ vibrate 'times' times. Each iteration will start vibrator 'on_time'
        milliseconds (up to 500, will be truncated if larger), and then stop it 'off_time'
        milliseconds (no limit here)"""
        on_time = min(500, on_time)

        for i in range(times):
            self.startVibration()
            time.sleep(on_time / 1000.0)
            self.stopVibration()
            time.sleep(off_time / 1000.0)

    def setGoal(self, steps):
        """ set the number of steps to that will be considered your daily goal """
        data = [0x05, 0x00, steps & 0xff, (steps >> 8) & 0xff]
        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s(data))

    def setCurrentSteps(self, steps):
        """ set the current step counter value to 'steps' """
        data = [0x10, steps & 0xff, (steps >> 8) & 0xff]
        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s(data))

    def locate(self):
        """ vibrate and flash leds to locate your miband """
        self.requester.write_by_handle(
            Handle.CONTROL_POINT, str(bytearray([0x08, 0x00])))

    def setAlarm1(self, when, smart=0, repeat=0):
        """ set the alarm 1 to 'when', see setAlarm for more info """
        self.setAlarm(1, 0, when, smart, repeat)

    def setAlarm2(self, when, smart=0, repeat=0):
        """ set the alarm 2 to 'when', see setAlarm for more info """
        self.setAlarm(1, 1, when, smart, repeat)

    def setAlarm3(self, when, smart=0, repeat=0):
        """ set the alarm 2 to 'when', see setAlarm for more info """
        self.setAlarm(1, 2, when, smart, repeat)

    def clearAlarm1(self, when, smart=0, repeat=0):
        """ clear the alarm 1 to _when_, see setAlarm for more info. """
        self.setAlarm(1, 0, when, smart, repeat)

    def clearAlarm2(self, when, smart=0, repeat=0):
        """ clear the alarm 2 to 'when', see setAlarm for more info """
        self.setAlarm(1, 1, when, smart, repeat)

    def clearAlarm3(self, when, smart=0, repeat=0):
        """ clear the alarm 3 to 'when', see setAlarm for more info """
        self.setAlarm(1, 2, when, smart, repeat)

    def setAlarm(self, enable, number, when, smart, repeat):
        """ enable or disable the alarm 'number' to 'when' (a datetime in the
        future). If you want a 'smart' wake up, then set 'smart' to
        1. 'repeat' could be mibanda.EVERYDAY, or a combination of
        days (i.e: SATURDAY | SUNDAY) """
        assert number in (0, 1, 2), "Invalid alarm id"
        smart = 30 if smart != 0 else 0
        repeat = min(Calendar.EVERYDAY, repeat)
        byteseq = [
            0x04, number, enable,
            (when.year - 2000) & 0xff, when.month - 1, when.day,
            when.hour, when.minute, when.second,
            smart, repeat,
        ]

        print "write:", byteseq
        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s(byteseq))

    def enableRealTimeSteps(self):
        """ enable realtime notifications about steps detection """
        data = [0x03, 0x01]
        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s(data))

    def disableRealTimeSteps(self):
        """ disable realtime notifications about steps detection """
        data = [0x03, 0x00]
        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s(data))

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


class BatteryInfo(object):
    """Holds the battery information for the Mi Band."""

    def __init__(self, data):
        fields = map(ord, data)

        #: Battery level (in percentage), ranges from 0 (discharged) to 100 (full).
        self.level = fields[0]

        #: Date of last charge.
        self.last_charged = datetime(
            fields[1] + 2000,
            fields[2] + 1,
            *fields[3:6])

        #: Counter of number of charges.
        self.charge_counter = fields[7] + (fields[8] << 8)

        status_names = {1: 'low', 2: 'medium', 3: 'full', 4: 'not charging'}

        #: Current battery status, one of ``low``, ``medium``, ``full``
        #: or ``not charging``.
        self.status = status_names.get(fields[9], "unknown")


class LEParams(object):
    def __init__(self, data):
        """Holds the current Bluetooth LE connection params."""

        fields = map(ord, data)

        #: Minimum connection internal, in ms.
        self.minimum_connection_interval = fields[0] + (fields[1] << 8)

        #: Maximum connection internal, in ms.
        self.maximum_connection_interval = fields[2] + (fields[3] << 8)

        #: Connection latency.
        self.latency = fields[4] + (fields[5] << 8)

        #: Connection timeout, in hundredths of a second.
        self.timeout = fields[6] + (fields[7] << 8)

        #: Connection interval.
        self.connection_interval = fields[8] + (fields[9] << 8)

        #: Advertisement interval.
        self.advertisement_interval = fields[10] + (fields[11] << 8)


class DeviceInfo(object):
    def __init__(self, data):
        """Hols some assorted device information."""

        fields = map(ord, data)

        #: Current firmware version.
        self.firmware_version = "{}.{}.{}.{}".format(*reversed(fields[-4:]))


class UUID(object):
    """Mi Band characteristic UUIDs constants."""

    #: Holds the device related information: firmware version, hardware revision, etc.
    DEVICE_INFO = "0000ff01-0000-1000-8000-00805f9b34fb"

    #: Holds the Bluetooth LE device name.
    DEVICE_NAME = "0000ff02-0000-1000-8000-00805f9b34fb"

    #: Holds the user related information: uuid, gender, age, height and
    #: weight. Used to make a permanent bond with the device.
    USER_INFO = "0000ff04-0000-1000-8000-00805f9b34fb"

    #: Special characteristic to do multiple tasks: LED/motor control,
    #: alarms, set current steps, step goal, etc.
    CONTROL_POINT = "0000ff05-0000-1000-8000-00805f9b34fb"

    #: Used to read current step count.
    STEPS = "0000ff06-0000-1000-8000-00805f9b34fb"

    #: Configuration of Bluetooth LE conection parameters.
    LE_PARAMS = "0000ff09-0000-1000-8000-00805f9b34fb"

    #: Used to get/set the date/time information on the device. Could not
    #: be read directly, first must be writen.
    DATE_TIME = "0000ff0a-0000-1000-8000-00805f9b34fb"

    #: Holds battery information: status, level, charge counter and last charge date.
    BATTERY = "0000ff0c-0000-1000-8000-00805f9b34fb"


class Handle(object):
    """
    .. warning:: These may change after a new firmware release, please use UUIDs
                 instead (when possible).

    Mi Band characteristic handlers.
    """

    #: Handle for UUID USER_INFO.
    USER_INFO = 0x19

    #: Handle for UUID CONTROL_POINT.
    CONTROL_POINT = 0x1b

    #: Handle for UUID DATE_TIME.
    DATE_TIME = 0x27

    #: Handle to do an automatic hardware test.
    TEST = 0x2e

    #: Handle for pairing device.
    PAIR = 0x33


class Calendar(object):
    """Constants used on alarm repeat pattern."""

    MONDAY     = 0b00000001
    TUESDAY    = 0b00000010
    WEDNESDAY  = 0b00000100
    THURSDAY   = 0b00001000
    FRIDAY     = 0b00010000
    SATURDAY   = 0b00100000
    SUNDAY     = 0b01000000
    EVERYDAY   = 0b01111111


class Colors(object):
    """Common colors of Mi Band LEDs. You can create new ones: a
    combination of three integers that range from 0 to 6 (both
    included). The higher the number the brighter the LED, 0 is LED off."""

    BLACK    = (0, 0, 0)
    BLUE     = (0, 0, 6)
    GREEN    = (0, 6, 0)
    AQUA     = (0, 6, 6)
    RED      = (6, 0, 0)
    FUCHSIA  = (6, 0, 6)
    YELLOW   = (6, 6, 0)
    GRAY     = (3, 3, 3)
    WHITE    = (6, 6, 6)
    ORANGE   = (6, 3, 0)


def h2s(data):
    """Converts a string of hex numbers separated by a colon (:) to a
    string with the actual byte sequence. This is useful when sending
    commands to PyGattlib, because they can be expressed in the same way as
    wireshark dumps them; in example: ``03:1b:05``. ::

      >>> data = mibanda.h2s("68:65:6c:6c:6f")
      >>> print data
      hello
    """

    if isinstance(data, str):
        data = map(lambda x: int(x, 16), data.split(":"))
    return str(bytearray(data))
