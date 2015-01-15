#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

import sys
import pyshark

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {} <capture_file>".format(sys.argv[0])
        sys.exit(-1)

    cap = pyshark.FileCapture(sys.argv[1])

    for i, pkt in enumerate(cap):
        cmd = getattr(pkt, "bthci_cmd", None)
        if cmd is not None:
            print "CMD:", cmd.get_field("opcode").showname
            continue

        evt = getattr(pkt, "bthci_evt", None)
        if evt is not None:
            print "EVT:", evt.get_field("code").showname
            continue

        att = getattr(pkt, "btatt", None)
        if att is not None:
            print "ATT:", att.get_field("opcode").showname
            continue

        print "Skipped packet"
