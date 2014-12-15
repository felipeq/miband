// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

#ifndef _MIBANDA_DEVICES_H_
#define _MIBANDA_DEVICES_H_

#define HANDLER_BATTERY 0x002b

#include "gattlib.h"
#include <vector>

class BatteryInfo {
public:
	BatteryInfo(std::string data);

	uint8_t level;
	tm last_charged;
	uint16_t charge_counter;

	typedef enum {
		low = 1,
		medium = 2,
		full = 3,
		notCharging = 4,
	} BatteryStatus;

	BatteryStatus status;
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
