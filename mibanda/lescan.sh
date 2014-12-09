#!/bin/bash
# -*- mode: sh; coding: utf-8 -*-

DEVICE=hci0
TIMEOUT=$1

if [ -z "$TIMEOUT" ]; then
    TIMEOUT=3
fi

sudo hciconfig $DEVICE down
sudo hciconfig $DEVICE up
sudo unbuffer hcitool -i $DEVICE lescan | grep ":" &

sleep $TIMEOUT
sudo killall -9 hcitool
