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
_LED_ON_OPCODE            =  0x1C
_LED_OFF_OPCODE           =  0x1D

DOOR_CLOSED = 90
DOOR_OPEN = 30
TRASH_CLOSED = 25
TRASH_OPEN = 60

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
        self.send(_WRITE_OUTDOOR_OPCODE,INT(DOOR_CLOSED))

    def open_outdoor(self):
        self.send(_WRITE_OUTDOOR_OPCODE,INT(DOOR_OPEN))

    def is_outdoor_closed(self):
        output = self.execute(_GET_OUTDOOR_OPCODE)
        outdoorAngle = output.read(INT)
        return bool(outdoorAngle == DOOR_CLOSED)

    def close_indoor(self):
        self.send(_WRITE_INDOOR_OPCODE,INT(DOOR_CLOSED))

    def open_indoor(self):
        self.send(_WRITE_INDOOR_OPCODE,INT(DOOR_OPEN))

    def is_indoor_closed(self):
        output = self.execute(_GET_INDOOR_OPCODE)
        indoorAngle = output.read(INT)
        return bool(indoorAngle == DOOR_CLOSED)

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

    def led_off(self):
        self.send(_LED_OFF_OPCODE,BYTE(1))

    def led_on(self):
        self.send(_LED_ON_OPCODE,BYTE(1))
