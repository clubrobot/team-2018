#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import math
from serialtalks import *
#from serialtalks import BYTE, INT, LONG, FLOAT
from components import SerialTalksProxy

# Instructions

GET_VELOCITY_OPCODE         = 0x04
GET_CONSTANT_OPCODE         = 0x05
GET_WHEELRADIUS_OPCODE      = 0x06
GET_MAX_VELOCITY_OPCODE     = 0x06

IS_ENABLED_OPCODE           = 0x07

SET_VELOCITY_OPCODE         = 0x08
SET_CONSTANT_OPCODE         = 0x09
SET_WHEELRADIUS_OPCODE      = 0x0A

ENABLE_OPCODE               = 0X0B
DISABLE_OPCODE              = 0X0C

LOAD_OPCODE                 = 0X0D
SAVE_OPCODE                 = 0X0E


class BrushlessMotor(SerialTalksProxy):
	def __init__(self, parent, uuid='BrushlessMotor'):
		SerialTalksProxy.__init__(self, parent, uuid)

	def get_velocity(self):
		output = self.execute(GET_VELOCITY_OPCODE)
		velocity = output.read(FLOAT)
		return velocity

	def get_constant(self):
		output = self.execute(GET_CONSTANT_OPCODE)
		constant = output.read(FLOAT)
		return constant

	def get_wheelRadius(self):
		output = self.execute(GET_WHEELRADIUS_OPCODE)
		wheelRadius = output.read(FLOAT)
		return wheelRadius

	def get_maxVelocity(self):
		output = self.execute(GET_MAX_VELOCITY_OPCODE)
		maxVelocity = output.read(FLOAT)
		return maxVelocity

	def is_enabled(self):
		output = self.execute(IS_ENABLED_OPCODE)
		flag = output.read(BYTE)
		return flag

	def set_velocity(self, velocity):
		self.send(SET_VELOCITY_OPCODE, FLOAT(velocity))

	def set_constant(self, constant):
		self.send(SET_CONSTANT_OPCODE, FLOAT(constant))

	def set_wheelRadius(self, wheelRadius):
		self.send(SET_WHEELRADIUS_OPCODE, FLOAT(wheelRadius))

	def enable(self):
		self.send(ENABLE_OPCODE)

	def disable(self):
		self.send(DISABLE_OPCODE)

	def load(self, adress):
		self.send(LOAD_OPCODE, INT(adress))

	def save(self, adress):
		self.send(SAVE_OPCODE, INT(adress))
