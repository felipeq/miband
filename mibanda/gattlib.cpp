// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

#include <iostream>
#include "gattlib.h"

GATTResponse::GATTResponse() {
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
	std::string msg = "Characteristic value/descriptor read failed:";
	msg += att_ecode2str(_status);
	throw std::runtime_error(msg);
    }

    return true;
}

std::string
GATTResponse::received() {
    return _data;
}

GATTRequester::GATTRequester(std::string address) :
    _address(address) {

}

static void
_read_by_handler_cb(guint8 status, const guint8* data, guint16 size, gpointer userp) {
    GATTResponse* response = (GATTResponse*)userp;
    response->notify(status, std::string(data, size));
}

void
GATTRequester::read_by_handler(uint16_t handle, GATTResponse* response) {

    // GAttrib *attrib = user_data;
    // gatt_read_char(attrib, handle, _read_by_handler_cb, (gpointer)response);
}
