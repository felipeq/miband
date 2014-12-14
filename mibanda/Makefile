# -*- mode: makefile-gmake; coding: utf-8 -*-

TARGETS  = services.so devices.so
OBJECTS  = devices.o gattlib.o
CFLAGS   = -ggdb -fPIC -Wall $$(python-config --includes)
CXXFLAGS = $(CFLAGS)
LDFLAGS  = -lboost_python -lbluetooth

all: $(TARGETS)

services.so: $(OBJECTS) services.o
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

devices.so: $(OBJECTS)
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

.PHONY: clean
clean:
	rm -f *.o *.so* *~
