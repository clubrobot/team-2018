#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import math

from serialtalks import BYTE, INT, LONG, FLOAT, SerialTalks


_WRITE_OUTDOOR_OPCODE = 0x13
_WRITE_INDOOR_OPCODE = 0X12
_WRITE_TRASH_OPCODE = 0X14
_SET_MOTOR_VELOCITY_OPCODE = 0x11
_GET_MOTOR_VELOCITY_OPCODE = 0x15

DOOR_CLOSED = 90
DOOR_OPEN = 30
TRASH_CLOSED = 25
TRASH_OPEN = 60

class Demo(SerialTalks):	
    def __init__(self, uuid='/dev/arduino/demo'):
        SerialTalks.__init__(self, uuid)

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

    def close_indoor(self):
        self.send(_WRITE_INDOOR_OPCODE,INT(DOOR_CLOSED))

    def open_indoor(self):
        self.send(_WRITE_INDOOR_OPCODE,INT(DOOR_OPEN))

    def close_trash(self):
        self.send(_WRITE_TRASH_OPCODE,INT(TRASH_CLOSED))

    def open_trash(self):
        self.send(_WRITE_TRASH_OPCODE,INT(TRASH_OPEN))

    def set_motor_velocity(self, speed):
        self.send(_SET_MOTOR_VELOCITY_OPCODE,INT(speed))

    def get_motor_velocity(self):
        output = self.execute(_GET_MOTOR_VELOCITY_OPCODE)
        velocity = output.read(INT)
        return int(velocity)