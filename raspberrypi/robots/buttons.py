#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
sys.path.append("../common/")


import time
import math

from serialtalks import BYTE, INT, LONG, FLOAT
from components import SerialTalksProxy

LED_ON_OPCODE	= 0x011
LED_OFF_OPCODE	= 0x012
class ButtonCard (SerialTalksProxy):
	BUTTON_ID = 1
	RED_BUTTON = 1
	GREEN_BUTTON = 2
	BLUE_BUTTON = 3
	YELLOW_BUTTON = 4
	EMERGENCY = 5
	PLAY_MODE = 6
	DEV_MODE = 7
	TIRETTE = 8

	def __init__(self, parent, uuid='buttonCard'):
		SerialTalksProxy.__init__(self, parent, uuid)
		self.functions = list()
		self.bind(1,self._compute)

	def _compute(self,bytes):

		self.function[bytes.read(BYTE)]()

	def affect(self,ID,function):
		self.functions[ID] = function

	def setLedOn(self, nb):
		self.send(LED_ON_OPCODE, BYTE(nb))

	def setLedOff(self,nb):
		self.send(LED_OFF_OPCODE, BYTE(nb))



