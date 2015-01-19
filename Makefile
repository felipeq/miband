# -*- mode: makefile-gmake; coding: utf-8 -*-

all:

.PHONY: clean
clean:
	find -name "*.pyc" -delete
	find -name "*~" -delete
	$(RM) -fr dist MANIFEST
