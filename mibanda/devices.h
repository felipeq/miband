// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

#ifndef _MIBANDA_DEVICES_H_
#define _MIBANDA_DEVICES_H_

#include <vector>

class BandDevice {
public:
    BandDevice(std::string address, std::string name);
    std::string getName();
    std::string getAddress();

private:
    std::string _address;
    std::string _name;
};

typedef boost::shared_ptr<BandDevice> BandDevicePtr;
typedef std::vector<BandDevicePtr> BandDeviceList;

#endif // _MIBANDA_DEVICES_H_
