#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import math

from serialtalks import BYTE, INT, LONG, FLOAT, BOOL, SerialTalks
from components import SerialTalksProxy


_SET_MOTOR_VELOCITY_OPCODE		= 0x17
_GET_MOTOR_VELOCITY_OPCODE		= 0x18
_SET_MOTOR_PULSEWIDTH_OPCODE	= 0x1A
_GET_MOTOR_PULSEWIDTH_OPCODE	= 0x1B

class WaterLauncher(SerialTalksProxy):	
	def __init__(self,parent, uuid='watershooter'):
		SerialTalksProxy.__init__(self, parent, uuid)

	def set_motor_velocity(self, velocity):
		output = self.execute(_SET_MOTOR_VELOCITY_OPCODE,INT(velocity))
		inSetup = output.read(BOOL)
		if(inSetup):
			msg = "Please wait, ESC in setup..."
		else:
			msg = ""
		return msg

	def get_motor_velocity(self):
		output = self.execute(_GET_MOTOR_VELOCITY_OPCODE)
		velocity = output.read(INT)
		return int(velocity)

	def set_distance_motor_velocity(self, distance_cm):
		velocity = distance_cm * 12/100
		self.set_motor_velocity(velocity)

	def set_motor_pulsewidth(self, pulsewidth):
		output = self.execute(_SET_MOTOR_PULSEWIDTH_OPCODE,INT(pulsewidth))
		inSetup = output.read(BOOL)
		if(inSetup):
			msg = "Please wait, ESC in setup..."
		else:
			msg = ""
		return msg

	def get_motor_pulsewidth(self):
		output = self.execute(_GET_MOTOR_PULSEWIDTH_OPCODE)
		return output.read(INT)