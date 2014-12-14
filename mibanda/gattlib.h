// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

#ifndef _MIBANDA_GATTLIB_H_
#define _MIBANDA_GATTLIB_H_

#include <string>
#include <stdint.h>

#include <boost/thread/mutex.hpp>

//
// FIXME: only a mutex is not valid, you need a condition variable
//

class Event {
public:
	Event() : _flag(false) {
	}

	void set() {
		_flag = true;
		_mutex.unlock();
	}

	void clear() {
		_flag = false;
	}

	bool wait(uint16_t timeout) {
		if (_flag)
			return _flag;

		if (timeout > 0)
			_mutex.timed_lock(timeout);
		else if (timeout == 0)
			_mutex.try_lock();
		else
			_mutex.lock();

		return _flag;
	}

private:
	bool _flag;
	boost::timed_mutex _mutex;
};

class GATTResponse {
public:

	GATTResponse();
	bool wait(uint16_t timeout);
	std::string received();

private:
	uint8_t _status;
	std::string _data;
	Event _event;
};

class GATTRequester {
public:

	GATTRequester(std::string address);
	void read_by_handler(uint16_t handle, GATTResponse& response);

private:
	std::string _address;
};

#endif // _MIBANDA_GATTLIB_H_
