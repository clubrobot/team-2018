#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
sys.path.append("../common/")

import time
import math

from serialtalks import BYTE, INT, LONG, FLOAT, SerialTalks
from components import SerialTalksProxy


_SET_MOTOR_VELOCITY_OPCODE		= 0x17
_GET_MOTOR_VELOCITY_OPCODE		= 0x18
_SET_MOTOR_PULSEWIDTH_OPCODE	= 0x1A
_GET_MOTOR_PULSEWIDTH_OPCODE	= 0x1B
_FORCE_PULSEWIDTH				= 0x1E

class WaterLauncher(SerialTalksProxy):	
	def __init__(self,parent, uuid='watershooter'):
		SerialTalksProxy.__init__(self, parent, uuid)

	def set_motor_velocity(self, velocity):
		output = self.execute(_SET_MOTOR_VELOCITY_OPCODE,INT(velocity))
		inSetup = output.read(INT)
		if not inSetup :
			return "Please wait, ESC in startup..."
		

	def get_motor_velocity(self):
		output = self.execute(_GET_MOTOR_VELOCITY_OPCODE)
		velocity = output.read(INT)
		return int(velocity)

	def set_distance_motor_velocity(self, distance_cm):
		velocity = distance_cm * 12/100
		self.set_motor_velocity(velocity)

	def set_motor_pulsewidth(self, pulsewidth):
		output = self.execute(_SET_MOTOR_PULSEWIDTH_OPCODE,INT(pulsewidth))
		inSetup = output.read(INT)
		if not inSetup:
			return "Please wait, ESC in startup..."

	def get_motor_pulsewidth(self):
		output = self.execute(_GET_MOTOR_PULSEWIDTH_OPCODE)
		return output.read(INT)

	def force_pulsewidth(self, pulsewidth):
		self.send(_FORCE_PULSEWIDTH, INT(pulsewidth))

	def setupPulsewidthESC(self):
		print("Please activate emergency stop")
		print("Press enter when ready");
		input()
		self.force_pulsewidth(2000);
		print("Please disable emergency stop and wait for 123 melody, 2 short beep")
		print("Press enter directly after the last 2 beep")
		input()
		self.force_pulsewidth(1000);
		print("Wait for 3 beep for battery cell count and a long final beep")
		print("End of ESC setup and motor ready to go !")