# -*- mode: makefile-gmake; coding: utf-8 -*-

TARGETS  = services.so devices.so
CFLAGS   = -ggdb -fPIC -Wall $$(python-config --includes)
CXXFLAGS = $(CFLAGS)
LDFLAGS  = -lboost_python -lbluetooth

all: $(TARGETS)

services.so: services.o devices.o
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

devices.so: devices.o
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

.PHONY: clean
clean:
	rm -f *.o *.so* *~
