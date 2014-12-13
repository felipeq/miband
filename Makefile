# -*- mode: makefile-gmake; coding: utf-8 -*-

all:
	make -C mibanda $@

.PHONY: clean
clean:
	find -name "*.pyc" -delete
	find -name "*~" -delete
	find -name "*.so" -delete
	find -name "*.o" -delete
