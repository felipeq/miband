#!/bin/bash
# -*- mode: sh; coding: utf-8 -*-

DST="88:0F:10:10:73:DA"

function write() {
    local handler=$1
    local value=$2

    gatttool -b "$DST" --char-write-req -a "$handler" -n "$value"
}

function read() {
    local handler=$1

    gatttool -b "$DST" --char-read -a "$handler"
}

write 0x0017 0100
write 0x001e 0100
write 0x0021 0100
write 0x002c 0100
write 0x0031 0100

