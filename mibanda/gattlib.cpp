// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

// Copyright (C) 2014, Oscar Acena <oscar.acena@uclm.es>
// This software is under the terms of GPLv3 or later.

#include <iostream>
#include <boost/python.hpp>
#include <boost/thread/thread.hpp>

#include "gattlib.h"

void
IOService::start() {
	boost::thread iothread(*this);
}

void
IOService::operator()() {
	GMainLoop *event_loop = g_main_loop_new(NULL, FALSE);

	g_main_loop_run(event_loop);
	g_main_loop_unref(event_loop);
}

void
GATTResponse::notify(uint8_t status, std::string data) {
    _status = status;
    _data = data;
    _event.set();
}

bool
GATTResponse::wait(uint16_t timeout) {
    if (not _event.wait(timeout))
		return false;

    if (_status != 0) {
		std::string msg = "Characteristic value/descriptor read failed: ";
		msg += att_ecode2str(_status);
		throw std::runtime_error(msg);
    }

    return true;
}

std::string
GATTResponse::received() {
    return _data;
}

void
connect_cb(GIOChannel* channel, GError* err, gpointer userp) {
	if (err) {
		std::string msg(err->message);
		g_error_free(err);
		throw std::runtime_error(msg);
	}

	GError *gerr = NULL;
	uint16_t mtu;
	uint16_t cid;
	bt_io_get(channel, &gerr,
			  BT_IO_OPT_IMTU, &mtu,
			  BT_IO_OPT_CID, &cid,
			  BT_IO_OPT_INVALID);

	// Can't detect MTU, using default
	if (gerr) {
		g_error_free(gerr);
	 	mtu = ATT_DEFAULT_LE_MTU;
	}

	if (cid == ATT_CID)
	 	mtu = ATT_DEFAULT_LE_MTU;

	GATTRequester* request = (GATTRequester*)userp;
	request->_attrib = g_attrib_new(channel, mtu);
}

GATTRequester::GATTRequester(std::string address) :
    _address(address),
	_channel(NULL),
	_attrib(NULL) {

	GError *gerr = NULL;
	_channel = gatt_connect
		("hci0",           // 'hciX'
		 address.c_str(),  // 'mac address'
		 "public",         // 'public' '[public | random]'
		 "low",            // 'low' '[low | medium | high]'
		 0,                // 0, int
		 0,                // 0, mtu
		 connect_cb,
		 &gerr,
		 (gpointer)this);

	if (_channel == NULL) {
	 	g_error_free(gerr);
		throw std::runtime_error(gerr->message);
	}
}

GATTRequester::~GATTRequester() {
	if (_channel != NULL) {
		g_io_channel_shutdown(_channel, TRUE, NULL);
		g_io_channel_unref(_channel);
	}

	if (_attrib != NULL) {
		g_attrib_unref(_attrib);
	}
}

static void
read_by_handler_cb(guint8 status, const guint8* data,
					guint16 size, gpointer userp) {
    GATTResponse* response = (GATTResponse*)userp;

	// First byte is the payload size
    response->notify(status, std::string((const char*)data + 1, size - 1));
}

void
GATTRequester::read_by_handle_async(uint16_t handle, GATTResponse* response) {
	check_channel();
    gatt_read_char(_attrib, handle, read_by_handler_cb, (gpointer)response);
}

std::string
GATTRequester::read_by_handle(uint16_t handle) {
	GATTResponse response;
	read_by_handle_async(handle, &response);

	if (not response.wait(MAX_WAIT_FOR_PACKET))
		// FIXME: now, response is deleted, but is still registered on
		// GLIB as callback!!
		throw std::runtime_error("Devices is not responding!");

	return response.received();
}

void
GATTRequester::write_by_handle(uint16_t handle, std::string data) {
	check_channel();
	gatt_write_cmd(_attrib, handle, (const uint8_t*)data.data(), data.size(), NULL, NULL);
}

void
GATTRequester::check_channel() {
	time_t ts = time(NULL);
	while (_channel == NULL || _attrib == NULL) {
		usleep(1000);
		if (time(NULL) - ts > MAX_WAIT_FOR_PACKET)
			throw std::runtime_error("Channel or attrib not ready");
	}
}

using namespace boost::python;
BOOST_PYTHON_MODULE(gattlib) {

	class_<GATTRequester>("GATTRequester", init<std::string>())
		.def("read_by_handle", &GATTRequester::read_by_handle)
		.def("read_by_handle_async", &GATTRequester::read_by_handle_async)
		.def("write_by_handle", &GATTRequester::write_by_handle)
    ;

	register_ptr_to_python<GATTResponse*>();

	class_<GATTResponse, boost::noncopyable>("GATTResponse")
		.def("wait", &GATTResponse::wait)
		.def("received", &GATTResponse::received)
	;
}
