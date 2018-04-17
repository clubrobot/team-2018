#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import math

from common.serialtalks import BYTE, INT, LONG, FLOAT, SerialTalks
from common.components import SerialTalksProxy

_WRITE_BEEACTIVATOR_OPCODE		=   0x27

class BeeActuator(SerialTalksProxy):	
	def __init__(self,parent, uuid='watershooter'):
		SerialTalksProxy.__init__(self,parent, uuid)
		self.closed_position = 165
		self.open_position = 75
	
	def write(self, value):
		self.send(_WRITE_BEEACTIVATOR_OPCODE,INT(value))
	
	def open(self):
		self.write(self.open_position)
	
	def close(self):
		self.write(self.closed_position)
	
	def detach(self):
		self.write(-1)