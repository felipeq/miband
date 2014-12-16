// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

// Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
// This software is under the terms of GPLv3 or later.

#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <datetime.h>

#include "devices.h"

BatteryInfo::BatteryInfo(std::string data) :
	level(255),
	last_charged(),
	charge_counter(-1),
	status(notCharging) {
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

	if (not response.wait(5))
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

struct ctime_tm_to_datetime {
	static PyObject* convert(const tm t) {
		return PyDateTime_FromDateAndTime
			(t.tm_year, t.tm_mon, t.tm_mday,
			 t.tm_hour, t.tm_min, t.tm_sec, 0);
	}
};

BOOST_PYTHON_MODULE(devices) {

	classList<BandDeviceList>("BandDeviceList");
	register_ptr_to_python<BandDevicePtr>();

    to_python_converter<tm, ctime_tm_to_datetime>();

	class_<BandDevice>("BandDevice", init<std::string, std::string>())
		.def("getName", &BandDevice::getName)
		.def("getAddress", &BandDevice::getAddress)
		.def("getBatteryInfo", &BandDevice::getBatteryInfo)
	;

	class_<BatteryInfo>("BatteryInfo", init<std::string>())
		.def_readonly("level", &BatteryInfo::level)
		.def_readonly("last_charged", &BatteryInfo::last_charged)
		.def_readonly("charge_counter", &BatteryInfo::charge_counter)
		.def_readonly("status", &BatteryInfo::status)
	;
}
