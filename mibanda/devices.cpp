// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "devices.h"
#include "debug.h"

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

void
BandDevice::getBatteryInfo() {
	GATTResponse response;
	_gatt.read_by_handler(HANDLER_BATTERY, &response);

	if (not response.wait(5))
		// FIXME: now, response is deleted, but is still registered on
		// GLIB as callback!!
		throw std::runtime_error("Devices is not responding!");

	std::string data = response.received();
	hexdump(data);
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
}
