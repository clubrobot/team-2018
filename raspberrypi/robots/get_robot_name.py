#!/usr/bin/env python3
# -*- coding: utf-8 -*-

BORNIBUS = 0
R128     = 1
UNKNOWN  = -1

ROBOT_ID = UNKNOWN
try:
    open("/opt/BORNIBUS")
    ROBOT_ID = BORNIBUS
except IOError:
    pass
try:
    if ROBOT_ID!=BORNIBUS:
        open("/opt/128")
        ROBOT_ID = R128
except IOError:
    pass