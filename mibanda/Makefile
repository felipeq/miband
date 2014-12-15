# -*- mode: makefile-gmake; coding: utf-8 -*-

TARGETS  = services.so devices.so
OBJECTS  = devices.o gattlib.o att.o crypto.o uuid.o gatt.o gattrib.o \
	   btio.o log.o utils.o

CFLAGS  += -ggdb -fPIC -Wall $$(python-config --includes) \
	   -Ibluez $$(pkg-config --cflags glib-2.0)
CFLAGS  += -DVERSION='"5.25"'
CXXFLAGS = $(CFLAGS)
LDFLAGS  = -lboost_python -lboost_thread -lbluetooth \
	   $$(pkg-config --libs glib-2.0)

vpath %.c bluez/attrib
vpath %.c bluez/src
vpath %.c bluez/src/shared
vpath %.c bluez/lib
vpath %.c bluez/btio

all: $(TARGETS)

services.so: $(OBJECTS) services.o
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

devices.so: $(OBJECTS)
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

.PHONY: clean
clean:
	rm -f *.o *.so* *~
