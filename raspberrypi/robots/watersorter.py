#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
sys.path.append("../common/")

import time
import math

from serialtalks import BYTE, INT, LONG, FLOAT, SerialTalks
from components import SerialTalksProxy


_WRITE_INDOOR_OPCODE      =  0x11
_GET_INDOOR_OPCODE        =  0x12
_WRITE_OUTDOOR_OPCODE     =  0x13
_GET_OUTDOOR_OPCODE       =  0X14
_WRITE_TRASH_OPCODE       =  0x15
_GET_TRASH_OPCODE         =  0x16
_GET_WATER_COLOR_OPCODE   =  0x19

INDOOR_DOOR_OPEN = 44
OUTDOOR_DOOR_OPEN = 50

OUTDOOR_DOOR_CLOSED = 90
INDOOR_DOOR_CLOSED = 20

TRASH_CLOSED = 128
TRASH_OPEN = 150

class WaterSorter(SerialTalksProxy):	
    def __init__(self,parent, uuid='watershooter'):
        SerialTalksProxy.__init__(self,parent, uuid)

    def write_outdoor(self, ouverture):
        self.send(_WRITE_OUTDOOR_OPCODE,INT(ouverture))

    def write_indoor(self, ouverture):
        self.send(_WRITE_INDOOR_OPCODE,INT(ouverture))

    def write_trash(self, ouverture):
        self.send(_WRITE_TRASH_OPCODE,INT(ouverture))

    def close_outdoor(self):
        self.send(_WRITE_OUTDOOR_OPCODE,INT(OUTDOOR_DOOR_CLOSED))

    def open_outdoor(self):
        self.send(_WRITE_OUTDOOR_OPCODE,INT(OUTDOOR_DOOR_OPEN))

    def is_outdoor_closed(self):
        output = self.execute(_GET_OUTDOOR_OPCODE)
        outdoorAngle = output.read(INT)
        return bool(outdoorAngle == OUTDOOR_DOOR_CLOSED)

    def close_indoor(self):
        self.send(_WRITE_INDOOR_OPCODE,INT(INDOOR_DOOR_CLOSED))

    def open_indoor(self):
        self.send(_WRITE_INDOOR_OPCODE,INT(INDOOR_DOOR_OPEN))

    def is_indoor_closed(self):
        output = self.execute(_GET_INDOOR_OPCODE)
        indoorAngle = output.read(INT)
        return bool(indoorAngle == INDOOR_DOOR_CLOSED)

    def close_trash(self):
        self.send(_WRITE_TRASH_OPCODE,INT(TRASH_CLOSED))

    def open_trash(self):
        self.send(_WRITE_TRASH_OPCODE,INT(TRASH_OPEN))

    def is_trash_closed(self):
        output = self.execute(_GET_TRASH_OPCODE)
        trashAngle = output.read(INT)
        return bool(trashAngle == TRASH_CLOSED)

    def get_water_color(self):
        output = self.execute(_GET_WATER_COLOR_OPCODE)
        color = output.read(INT, INT, INT)
        return color