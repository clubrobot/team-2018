#!/usr/bin/env python3
# -*- coding: utf-8 -*-

BORNIBUS = 0
R128     = 1
UNKNOWN  = -1

ROBOT_ID = UNKNOWN
try:
    f = open("/opt/BORNIBUS")
    ROBOT_ID = BORNIBUS
    f.close()
except IOError:
    pass
try:
    if ROBOT_ID!=BORNIBUS:
        f = open("/opt/128")
        ROBOT_ID = R128
        f.close()
except IOError:
    pass