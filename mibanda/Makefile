# -*- mode: makefile-gmake; coding: utf-8 -*-

TARGET   = services.so
CFLAGS   = -ggdb -fPIC -Wall $$(python-config --includes)
CXXFLAGS = $(CFLAGS)
LDFLAGS  = -lboost_python -lbluetooth

all: $(TARGET)

$(TARGET): services.o
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

.PHONY: clean
clean:
	rm -f *.o *.so* *~
