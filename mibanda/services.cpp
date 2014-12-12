// -*- mode: c++; coding: utf-8; tab-width: 4 -*- 

#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>

#include <exception>
#include <boost/python.hpp>


class DiscoveryService {
public:
  DiscoveryService(std::string device, int timeout) {
	// get device number
    int dev_id = hci_devid(device.c_str());
	if (dev_id < 0) 
	  throw std::runtime_error("Invalid device!");

	// open device
	int dev_desc = hci_open_dev(dev_id);
	if (dev_desc < 0) 
	  throw std::runtime_error("Could not open device!");

	// set scan parameters
	int result;
	uint8_t scan_type = 0x01;
	uint16_t interval = htobs(0x0010);
	uint16_t window = htobs(0x0010);
	uint8_t own_type = 0x00;
	uint8_t filter_policy = 0x00;

	result = hci_le_set_scan_parameters
	  (dev_desc, scan_type, interval, window,
	   own_type, filter_policy, 10000);
	if (result < 0) 
	  throw std::runtime_error
		("Set scan parameters failed (are you root?)");

	// enable scan
	uint8_t filter_dup = 1;

	result = hci_le_set_scan_enable(dev_desc, 0x01, filter_dup, 10000);
	if (result < 0) 
	  throw std::runtime_error("Enable scan failed");

	// read advertisement messages
	// disable scan

	// close device
	hci_close_dev(dev_desc);
  }

  void discover() {
    
  }
};

using namespace boost::python;
BOOST_PYTHON_MODULE(services) {
  
  class_<DiscoveryService>("DiscoveryService", 
						   init<std::string, int>())
    .def("discover", &DiscoveryService::discover)
  ;
}

