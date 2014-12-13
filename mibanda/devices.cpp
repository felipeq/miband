// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "devices.h"

BandDevice::BandDevice(std::string address, std::string name) :
	_address(address),
	_name(name) {
}

std::string
BandDevice::getName() {
	return _name;
}

std::string
BandDevice::getAddress() {
	return _address;
}

bool
BandDevice::operator==(const BandDevice& other) {
	return _name == other._name and
		_address == other._address;
}

using namespace boost::python;
BOOST_PYTHON_MODULE(devices) {

	class_<BandDeviceList>("BandDeviceList")
        .def(vector_indexing_suite<BandDeviceList>() )
	;

	class_<BandDevice>("BandDevice", init<std::string, std::string>())
		.def("getName", &BandDevice::getName)
		.def("getAddress", &BandDevice::getAddress)
	;
}
