#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
sys.path.append("../common/")

import time
import math

from serialtalks import *
from components import SerialTalksProxy

# Instructions

UPDATE_ANCHOR_NUMBER_OPCODE = 0x10
UPDATE_ANTENNA_DELAY_OPCODE = 0x11
CALIBRATION_ROUTINE_OPCODE = 0x12
UPDATE_COLOR_OPCODE = 0x13
GET_POSITION_OPCODE = 0x14


class Anchor(SerialTalksProxy):

	def __init__(self, parent, uuid='anchor'):
		SerialTalksProxy.__init__(self, parent, uuid)

	def update_beacon_number(self, number):
		self.send(UPDATE_ANCHOR_NUMBER_OPCODE,BYTE(number))
		print(self.getout(timeout=1))
	
	def update_antenna_delay(self, delay):
		self.send(UPDATE_ANTENNA_DELAY_OPCODE,INT(delay))
		print(self.getout(timeout=1))

#	real_distance in mm, timeout in ms
	def calibrate(self,real_distance, timeout):
		self.send(CALIBRATION_ROUTINE_OPCODE,INT(real_distance),ULONG(timeout))
		print(self.getout(timeout=1))

#green : 0, orange : 1
	def update_color(self,real_distance, color):
		self.send(UPDATE_COLOR_OPCODE,INT(color))

	def get_potision(self,real_distance):
		output = self.execute(GET_POSITION_OPCODE)
		x, y = output.read(INT, INT)
		return x, y		
	

