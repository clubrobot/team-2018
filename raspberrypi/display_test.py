#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import math

from serialtalks import BYTE, INT, CHAR, LONG, STRING
from components import SerialTalksProxy

# Instructions

SET_DATA_OPCODE   = 0x10


class LEDMatrixTest(SerialTalksProxy):
	
	def __init__(self, parent, uuid='display'):
		SerialTalksProxy.__init__(self, parent, uuid)

	def set_data(self, data):
		self.send(SET_DATA_OPCODE, LONG(data))