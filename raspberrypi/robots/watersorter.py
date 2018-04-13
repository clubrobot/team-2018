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
_GET_SHAKER_HORIZONTAL_OPCODE    =      0x1F
_WRITE_SHAKER_HORIZONTAL_OPCODE  =      0x20
_GET_SHAKER_VERTICAL_OPCODE      =      0x21
_WRITE_SHAKER_VERTICAL_OPCODE    =      0x22
_GET_TRASH_UNLOADER_OPCODE       =      0x23
_WRITE_TRASH_UNLOADER_OPCODE     =      0x24
_ENABLE_SHAKING_OPCODE           =      0x25
_DISABLE_SHAKING_OPCODE          =      0x26

INDOOR_DOOR_OPEN = 44
OUTDOOR_DOOR_OPEN = 50

OUTDOOR_DOOR_CLOSED = 90
INDOOR_DOOR_CLOSED = 20

TRASH_CLOSED = 126
TRASH_OPEN = 150

SHAKER_HORIZONTAL_1 = 0
SHAKER_HORIZONTAL_2 = 135

SHAKER_VERTICAL_1 = 80
SHAKER_VERTICAL_2 = 95

TRASH_UNLOADER_OPEN = 125
TRASH_UNLOADER_CLOSED = 80

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
        self.send(_WRITE_TRASH_OPCODE,INT(60))
        time.sleep(0.2)
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

    def write_shaker_horizontal(self, ouverture):
        self.send(_WRITE_SHAKER_HORIZONTAL_OPCODE,INT(ouverture))

    def write_shaker_vertical(self, ouverture):
        self.send(_WRITE_SHAKER_VERTICAL_OPCODE,INT(ouverture))

    def write_trash_unloader(self, ouverture):
        self.send(_WRITE_TRASH_UNLOADER_OPCODE,INT(ouverture))

    def get_shaker_horizontal(self):
        output = self.execute(_GET_SHAKER_HORIZONTAL_OPCODE)
        return output.read(INT)
    
    def get_shaker_vertical(self):
        output = self.execute(_GET_SHAKER_VERTICAL_OPCODE)
        return output.read(INT)

    def get_trash_unloader(self):
        output = self.execute(_GET_TRASH_UNLOADER_OPCODE)
        return output.read(INT)

    def open_trash_unloader(self):
        self.write_trash_unloader(TRASH_UNLOADER_OPEN)

    def close_trash_unloader(self):
        self.write_trash_unloader(TRASH_UNLOADER_CLOSED)

    def enable_shaker(self):
        self.send(_ENABLE_SHAKING_OPCODE)

    def disable_shaker(self):
        self.send(_DISABLE_SHAKING_OPCODE)