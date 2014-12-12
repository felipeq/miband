// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

#include <boost/python.hpp>

class BandDevice {
public:
	BandDevice(std::string address, std::string name) :
		_address(address),
		_name(name) {
	}

private:
	std::string _address;
	std::string _name;
};

using namespace boost::python;
BOOST_PYTHON_MODULE(devices) {

	class_<BandDevice>("BandDevice", init<std::string, std::string>())
	;
}
