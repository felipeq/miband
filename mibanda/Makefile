# -*- mode: makefile-gmake; coding: utf-8 -*-

TARGETS  = services.so devices.so
OBJECTS  = devices.o gattlib.o

CFLAGS  += -ggdb -fPIC -Wall $$(python-config --includes) \
	   -Ibluez $$(pkg-config --cflags glib-2.0)
CXXFLAGS = $(CFLAGS)
LDFLAGS  = -lboost_python -lbluetooth \
	   $$(pkg-config --libs glib-2.0)

all: $(TARGETS)

services.so: $(OBJECTS) services.o
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

devices.so: $(OBJECTS)
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

.PHONY: clean
clean:
	rm -f *.o *.so* *~
