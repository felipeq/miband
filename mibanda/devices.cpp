// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

// Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
// This software is under the terms of GPLv3 or later.

#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "devices.h"

BatteryInfo::BatteryInfo(std::string data) :
	level(255),
	last_charged(),
	charge_counter(-1),
	status("unknown") {

	level = (int)data[0];
	last_charged.year = (int)data[1] + 2000;
	last_charged.month = (int)data[2];
	last_charged.day = (int)data[3];
	last_charged.hour = (int)data[4];
	last_charged.minute = (int)data[5];
	last_charged.second = (int)data[6];
	charge_counter = (int)data[7] + ((int)data[8] << 8);

	switch(data[9]) {
	case 1: status = "low"; break;
	case 2: status = "medium"; break;
	case 3: status = "full"; break;
	case 4: status = "not charging"; break;
	}
}

BandDevice::BandDevice(std::string address, std::string name) :
	_address(address),
	_name(name),
	_gatt(address) {
}

std::string
BandDevice::getName() {
	return _name;
}

std::string
BandDevice::getAddress() {
	return _address;
}

BatteryInfo
BandDevice::getBatteryInfo() {
	GATTResponse response;
	_gatt.read_by_handler(HANDLER_BATTERY, &response);

	std::cout << "wait response" << std::endl;

	if (not response.wait(MAX_WAIT_FOR_PACKET))
		// FIXME: now, response is deleted, but is still registered on
		// GLIB as callback!!
		throw std::runtime_error("Devices is not responding!");

	return BatteryInfo(response.received());
}

using namespace boost::python;

template < class T >
void classList(std::string name) {
    class_< T >(name.c_str(), no_init)
		.def("__iter__", iterator< T >())
		.def("__len__", &T::size)
    ;
}

BOOST_PYTHON_MODULE(devices) {

	classList<BandDeviceList>("BandDeviceList");
	register_ptr_to_python<BandDevicePtr>();

	class_<BandDevice>("BandDevice", init<std::string, std::string>())
		.def("getName", &BandDevice::getName)
		.def("getAddress", &BandDevice::getAddress)
		.def("getBatteryInfo", &BandDevice::getBatteryInfo)
	;

	class_<DateTime>("DateTime")
		.def_readonly("year", &DateTime::year)
		.def_readonly("month", &DateTime::month)
		.def_readonly("day", &DateTime::day)
		.def_readonly("hour", &DateTime::hour)
		.def_readonly("minute", &DateTime::minute)
		.def_readonly("second", &DateTime::second)
    ;

	class_<BatteryInfo>("BatteryInfo", init<std::string>())
		.def_readonly("level", &BatteryInfo::level)
		.def_readonly("last_charged", &BatteryInfo::last_charged)
		.def_readonly("charge_counter", &BatteryInfo::charge_counter)
		.def_readonly("status", &BatteryInfo::status)
	;
}
