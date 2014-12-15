// -*- mode: c++; coding: utf-8; tab-width: 4 -*-

#ifndef _MIBAND_DEBUG_H_
#define _MIBAND_DEBUG_H_

static void
hexdump(std::string data) {
    const char* c = data.data();
    for (unsigned int i=0; i<data.length(); i++) {
	int d = (int)*(c + i) & 0xff;
	std::cout << std::hex << d << " ";
    }
    std::cout << std::endl;
}

#endif // _MIBAND_DEBUG_H_
