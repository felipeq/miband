// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

// Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
// This software is under the terms of GPLv3 or later.

#ifndef _MIBANDA_DEVICES_H_
#define _MIBANDA_DEVICES_H_

#define HANDLER_BATTERY 0x002b

#include "gattlib.h"
#include <vector>

class DateTime {
public:
	int year;
	int month;
	int day;
	int hour;
	int minute;
	int second;
};

class BatteryInfo {
public:
	BatteryInfo(std::string data);

	uint8_t level;
	DateTime last_charged;
	uint16_t charge_counter;
	std::string status;
};

class BandDevice {
public:
    BandDevice(std::string address, std::string name);
    std::string getName();
    std::string getAddress();

	BatteryInfo getBatteryInfo();

private:
    std::string _address;
    std::string _name;
	GATTRequester _gatt;
};

typedef boost::shared_ptr<BandDevice> BandDevicePtr;
typedef std::vector<BandDevicePtr> BandDeviceList;

#endif // _MIBANDA_DEVICES_H_
