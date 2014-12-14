// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

#include <iostream>
#include <glib.h>

#include "gattlib.h"

extern "C" {
#include "lib/uuid.h"
#include "attrib/att.h"
#include "attrib/gattrib.h"
#include "attrib/gatt.h"
}

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

GATTRequester::GATTRequester(std::string address) :
    _address(address) {

}

static void
_read_by_handler_cb(guint8 status, const guint8* data,
					guint16 size, gpointer userp) {
    GATTResponse* response = (GATTResponse*)userp;
    response->notify(status, std::string((const char*)data, size));
}

void
GATTRequester::read_by_handler(uint16_t handle, GATTResponse* response) {

	GIOChannel* io;
	GError* gerr = NULL;

	// FIXME: gatt_connect will be called from IO thread. The
	// connect_cb is called with the results (the created io
	// channel). Then, this Requester could create the attribute, and
	// use it.

	io = gatt_connect(opt_src,       // 'hci0'
					  opt_dst,       // 'mac address'
					  opt_dst_type,  // 'public' '[public | random]'
					  opt_sec_level, // 'low' '[low | medium | high]'
					  opt_psm,       // 0, int
					  opt_mtu,       // 0, mtu
					  connect_cb,
					  &gerr);

	if (chann == NULL) {
		g_error_free(gerr);
		throw std::runtime_error(gerr->message);
	}

	uint16_t mtu;
	uint16_t cid;
	bt_io_get(io, &gerr,
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

	GAttrib* attrib = g_attrib_new(io, mtu);
	gatt_read_char(attrib, handle, _read_by_handler_cb, (gpointer)response);
}
