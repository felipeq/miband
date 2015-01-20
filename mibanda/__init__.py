# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
# This software is under the terms of GPLv3 or later.

import time
from datetime import datetime
import struct
import gattlib


class DiscoveryService(object):
    """Service to discover Mi Band devices nearby using Bluetooth LE.

    ``device`` is the name of your Bluetooth hardware (could be get
    using ``hciconfig``). If not given, the first device is used:
    *hci0*. ::

      >>> sd = mibanda.DiscoveryService()

    .. note:: It may require superuser privileges (run as root, or using sudo).
    """

    def __init__(self, device="hci0"):
        self.service = gattlib.DiscoveryService(device)

    def discover(self, timeout=3):
        """Launch the discovery process. It runs a LE scan to discover new
        devices, up to ``timeout`` seconds. It returns a list with newly
        created :class:`mibanda.BandDevice` objects, one for each discovered
        Mi Band. ::

          >>> sd.discover()
          [<mibanda.BandDevice at 0x7f03fcd54c50>]
        """

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
        """Used to create a connection with the Mi Band. It may take some
        time, depending on many factors as LE params, channel usage,
        etc. ::

          >>> device.connect()

        .. note:: This method needs to be called before almost any
                  other command. Also note that the connection will be
                  closed after some period of inactivity. See
                  Bluetooth LE params for more info.
        """

        self.requester.connect(True)

    def getAddress(self):
        """Get device's MAC address. Is the same value given at construction
        time. It's a fixed param. ::

          >>> device.getAddress()
          '88:0F:10:00:01:02'
        """

        return self.address

    def getName(self, cached=True):
        """Get device's Bluetooth name. Usually the string 'MI', but it may be
        changed. It will return the name given at construction time,
        or read the device's name. This name will be cached, but you
        can force the read passing *False* on ``cached`` argument. ::

          >>> device.getName()
          'MI'
        """

        if cached and self.name:
            return self.name

        self.name = self.requester.read_by_uuid(UUID.DEVICE_NAME)[0]
        return self.name

    def getBatteryInfo(self):
        """Get information about device battery. Returns a
        :class:`mibanda.BatteryInfo` instance. ::

          >>> info = device.getBatteryInfo()
          >>> info.status
          'not charging'
          >>> info.level
          86
          >>> info.charge_counter
          6
          >>> info.last_charged
          datetime.datetime(2015, 1, 11, 22, 36)
        """

        data = self.requester.read_by_uuid(UUID.BATTERY)
        return BatteryInfo(data[0])

    def getDeviceInfo(self):
        """Get device information: firmware version, etc.
        ::

          >>> info = device.getDeviceInfo()
          >>> info.firmware_version
          '1.0.6.2'
        """

        data = self.requester.read_by_uuid(UUID.DEVICE_INFO)[0]
        return DeviceInfo(data)

    def getSteps(self):
        """Get current step counter value. This is the device counter, as
        shown in the official application. Returns an integer. ::

          >>> device.getSteps()
          4730
        """

        data = self.requester.read_by_uuid(UUID.STEPS)[0]
        return ord(data[0]) + (ord(data[1]) << 8)

    def getLEParams(self):
        """Get Bluetooth LE connection parameters. This parameters are
        negotiated at connection stablishment, and can be updated
        later through a connection update. Returns a new
        :class:`mibanda.LEParams` instance. ::

          >>> le = device.getLEParams()
          >>> le.minimum_connection_interval
          460
          >>> le.maximum_connection_interval
          500
          >>> le.latency
          0
          >>> le.timeout
          500
          >>> le.connection_interval
          500
          >>> le.advertisement_interval
          2400
        """

        data = self.requester.read_by_uuid(UUID.LE_PARAMS)[0]
        return LEParams(data)

    def setDateTime(self, dt=None):
        """Set current device date and time, ``dt`` is a ``datetime.datetime`` object.

        .. note:: This method requires the device to be configured
                  with UserInfo. Otherwise, it will raise an ``Application error:
                  I/O``. See :meth:`mibanda.BandDevice.setUserInfo` for more info.
        ::

          >>> from datetime import datetime
          >>> now = datetime.now()
          >>> device.setDateTime(now)
        """

        if dt is None:
            dt = datetime.now()

        data = [(dt.year - 2000) & 0xff, dt.month - 1, dt.day,
                dt.hour, dt.minute, dt.second]

        self.requester.write_by_handle(Handle.DATE_TIME, str(bytearray(data)))

    def getDateTime(self):
        """Get current device date and time. This characteristic could not be
        read directly; it need to be writen first, and then read. This
        process adds a bit of lag: the time of traveling packets. It
        returns a ``datetime.datetime`` object.

        .. note:: This method requires the device to be configured
                  with UserInfo. Otherwise, it will raise an ``Application error:
                  I/O``. See :meth:`mibanda.BandDevice.setUserInfo` for more info.
        ::

          >>> device.getDateTime()
          datetime.datetime(2015, 1, 20, 21, 28, 30, 0)

        """

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
        """Perform an internat test: it will vibrate and flash leds.

        .. warning:: This action will erase status information on your device.
        ::

          >>> device.selfTest()
        """

        self.requester.write_by_handle(Handle.TEST, str(bytearray([2])))

    def pair(self):
        """Make a bluetooth pair between this host's hardware and the Mi Band
        device. ::

          >>> device.pair()
        """

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
        """Set user information on device. This params as a whole are needed
        to avoid a status reset on the Mi Band. If you change any of
        this params, the Mi Band will erase all previous capture data,
        and initiate a new pairing process.

        ``uid`` is a number that identifies the relationship between
        this host and this Mi Band. It may be any number, but it must
        have 10 or less digits.

        ``male`` is a boolean param to set the user gender.

        ``age`` is your age in years.

        ``height`` is your height in centimeters.

        ``weight`` is your weight in kilograms.

        ``type_`` is a binary int (0 or 1) that specify if this
        relationship should be rebuilt (1) or not (0). If 1, all saved
        data will be lost.

        ``alias`` this is a stringfied version of the ``uid``. You can
        safely left it blank, as it will be computed from the given
        ``uid``. ::

          >>> device.setUserInfo(1563037356, True, 25, 180, 80, 0)
        """

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
        """Toggle LED status for a few seconds, using values for red (``r``),
        green (``g``) and blue (``b``), levels range from 0 (LED off)
        to 6 (max bright). You can use the :class:`mibanda.Colors`
        predefined colors.

        .. note:: This method requires the device to be configured
                  with UserInfo. Otherwise, it will raise an ``Application error:
                  I/O``. See :meth:`mibanda.BandDevice.setUserInfo` for more info.
        ::

          >>> # set red color
          >>> device.flashLeds(6, 0, 0)

          >>> # set orange
          >>> device.flashLeds(*miband.Colors.ORANGE)
        """

        self.requester.write_by_handle(
            Handle.CONTROL_POINT, str(bytearray([0x0e, r, g, b, 0x01])))

    def startVibration(self):
        """Put the band in vibration mode up to 10 seconds, or until you
        tap the band.

        .. note:: This method requires the device to be configured
                  with UserInfo. Otherwise, it will raise an ``Application error:
                  I/O``. See :meth:`mibanda.BandDevice.setUserInfo` for more info.
        ::

          >>> device.startVibration()
        """

        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s("8:1"))

    def stopVibration(self):
        """Stop the vibration mode, if running.

        .. note:: This method requires the device to be configured
                  with UserInfo. Otherwise, it will raise an ``Application error:
                  I/O``. See :meth:`mibanda.BandDevice.setUserInfo` for more info.
        ::

          >>> device.stopVibration()
        """

        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s("13"))

    def customVibration(self, times, on_time, off_time):
        """Vibrate ``times`` times. Each iteration will start vibrator
        ``on_time`` milliseconds (up to 500, will be truncated if
        larger), and then stop it ``off_time`` milliseconds (no limit
        here).

        .. note:: This method requires the device to be configured
                  with UserInfo. Otherwise, it will raise an ``Application error:
                  I/O``. See :meth:`mibanda.BandDevice.setUserInfo` for more info.
        ::

          >>> # faster vibration (10 times)
          >>> device.customVibration(10, 25, 10)

          >>> # water drop vibration (5 times)
          >>> device.customVibration(5, 25, 1200)

          >>> # longer vibrations, no 'off time' (5 times)
          >>> device.customVibration(5, 500, 0)
        """

        on_time = min(500, on_time)

        for i in range(times):
            self.startVibration()
            time.sleep(on_time / 1000.0)
            self.stopVibration()
            time.sleep(off_time / 1000.0)

    def setGoal(self, steps):
        """Set the number of steps to ``steps`` to what will be considered
        your daily goal.

        .. note:: This method requires the device to be configured
                  with UserInfo. Otherwise, it will raise an ``Application error:
                  I/O``. See :meth:`mibanda.BandDevice.setUserInfo` for more info.
        ::

          >>> device.setGoal(8000)
        """

        data = [0x05, 0x00, steps & 0xff, (steps >> 8) & 0xff]
        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s(data))

    def setCurrentSteps(self, steps):
        """Set the current step counter value to ``steps``. It may be used to
        reset the counter.

        .. note:: This method requires the device to be configured
                  with UserInfo. Otherwise, it will raise an ``Application error:
                  I/O``. See :meth:`mibanda.BandDevice.setUserInfo` for more info.
        ::

          >>> setCurrentSteps(0)
        """

        data = [0x10, steps & 0xff, (steps >> 8) & 0xff]
        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s(data))

    def locate(self):
        """Vibrate and flash LEDs to locate your miband."""
        self.requester.write_by_handle(
            Handle.CONTROL_POINT, str(bytearray([0x08, 0x00])))

    def setAlarm1(self, when, smart=0, repeat=0):
        """Set the alarm 1 to 'when', see :meth:`mibanda.BandDevice.setAlarm`
        for more info."""
        self.setAlarm(1, 0, when, smart, repeat)

    def setAlarm2(self, when, smart=0, repeat=0):
        """Set the alarm 2 to 'when', see :meth:`mibanda.BandDevice.setAlarm`
        for more info."""
        self.setAlarm(1, 1, when, smart, repeat)

    def setAlarm3(self, when, smart=0, repeat=0):
        """Set the alarm 3 to 'when', see :meth:`mibanda.BandDevice.setAlarm`
        for more info."""
        self.setAlarm(1, 2, when, smart, repeat)

    def clearAlarm1(self, when, smart=0, repeat=0):
        """Clear the alarm 1, see :meth:`mibanda.BandDevice.setAlarm`
        for more info."""
        self.setAlarm(1, 0, when, smart, repeat)

    def clearAlarm2(self, when, smart=0, repeat=0):
        """Clear the alarm 2, see :meth:`mibanda.BandDevice.setAlarm`
        for more info."""
        self.setAlarm(1, 1, when, smart, repeat)

    def clearAlarm3(self, when, smart=0, repeat=0):
        """Clear the alarm 3, see :meth:`mibanda.BandDevice.setAlarm`
        for more info."""
        self.setAlarm(1, 2, when, smart, repeat)

    def setAlarm(self, enable, number, when, smart, repeat):
        """Enable or disable the alarm ``number`` to ``when`` (a
        datetime.datetime object in the future). If you want a 'smart'
        wake up, then set ``smart`` to 1. ``repeat`` could be
        mibanda.Calendar.EVERYDAY, or a combination of days (i.e:
        SATURDAY | SUNDAY).

        .. note:: This method requires the device to be configured
                  with UserInfo. Otherwise, it will raise an ``Application error:
                  I/O``. See :meth:`mibanda.BandDevice.setUserInfo` for more info.
        ::

          >>> when = datetime.now() + timedelta(hours=8)
          >>> device.setAlarm(1, 0, when, 0, mibanda.Calendar.MONDAY)
        """

        assert number in (0, 1, 2), "Invalid alarm id"
        smart = 30 if smart != 0 else 0
        repeat = min(Calendar.EVERYDAY, repeat)
        byteseq = [
            0x04, number, enable,
            (when.year - 2000) & 0xff, when.month - 1, when.day,
            when.hour, when.minute, when.second,
            smart, repeat,
        ]

        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s(byteseq))

    def enableRealTimeSteps(self):
        """Enable realtime notifications about steps detection."""
        data = [0x03, 0x01]
        self.requester.write_by_handle(Handle.CONTROL_POINT, h2s(data))

    def disableRealTimeSteps(self):
        """Disable realtime notifications about steps detection."""
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
