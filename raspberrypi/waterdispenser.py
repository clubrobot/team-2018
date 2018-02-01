#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import math

from serialtalks import BYTE, INT, LONG, FLOAT
from components import SerialTalksProxy

_DROP_OPCODE   = 0x10
_FIRE_OPCODE   = 0x20


class WaterDispenser(SerialTalksProxy):	
    def __init__(self, parent, uuid='waterdispenser'):
        SerialTalksProxy.__init__(self, parent, uuid)

    def fire(self):
        self.send(_FIRE_OPCODE)
    
    def drop(self):
        self.send(_DROP_OPCODE)