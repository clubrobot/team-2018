#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import math

from serialtalks import BYTE, INT, LONG, FLOAT, SerialTalks
from components import SerialTalksProxy


_SET_MOTOR_VELOCITY_OPCODE		= 0x17
_GET_MOTOR_VELOCITY_OPCODE		= 0x18
_SET_MOTOR_PULSEWIDTH_OPCODE	= 0x20

class WaterLauncher(SerialTalksProxy):	
    def __init__(self, uuid='/dev/arduino/watersorter'):
        SerialTalksProxy.__init__(self, uuid)

    def set_motor_velocity(self, velocity):
        self.send(_SET_MOTOR_VELOCITY_OPCODE,INT(velocity))

    def get_motor_velocity(self):
        output = self.execute(_GET_MOTOR_VELOCITY_OPCODE)
        velocity = output.read(INT)
        return int(velocity)

    def set_distance_motor_velocity(self, distance_cm):
        velocity = distance_cm * 12/100
        self.set_motor_velocity(velocity)

	def set_motor_pulsewidth(self, pulsewidth):
		self.send(_SET_MOTOR_PULSEWIDTH_OPCODE, INT(pulsewidth))