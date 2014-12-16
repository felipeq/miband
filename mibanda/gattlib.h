// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

// Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
// This software is under the terms of GPLv3 or later.

#ifndef _MIBANDA_GATTLIB_H_
#define _MIBANDA_GATTLIB_H_

#include <string>
#include <stdint.h>
#include <glib.h>

#include "event.hpp"

class IOService {
public:
	void start();
	void operator()();
};

class GATTResponse {
public:
	void notify(uint8_t status, std::string data);
	bool wait(uint16_t timeout);
	std::string received();

private:
	uint8_t _status;
	std::string _data;
	Event _event;
};

void connect_cb(GIOChannel* channel, GError* err, gpointer user_data);

class GATTRequester {
public:
	GATTRequester(std::string address);
	~GATTRequester();
	void read_by_handler(uint16_t handle, GATTResponse* response);

	friend void connect_cb(GIOChannel*, GError*, gpointer);

private:
	std::string _address;
	GIOChannel* _channel;
};

#endif // _MIBANDA_GATTLIB_H_
