#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
sys.path.append("../common/")

import time
import math

from serialtalks import BYTE, INT, LONG, FLOAT
from components import SerialTalksProxy

# Instructions

_GET_MESURE_SENSOR_OPCODE    = 0x10
_ACTIVATE_SENSORS_OPCODE 	 = 0x11
_DESACTIVATE_SENSORS_OPCODE  = 0x12
_GET_NORMAL_OPCODE           = 0x13

class Sensors(SerialTalksProxy):
	def __init__(self, parent, uuid='sensors'):
		SerialTalksProxy.__init__(self, parent, uuid)

	def get_normal(self,delta_time):
		output = self.execute(_GET_NORMAL_OPCODE,INT(delta_time))
		av_std, av_var, ar_std, ar_var = output.read(FLOAT, FLOAT, FLOAT, FLOAT)
		return ((av_std,av_var),(ar_std,ar_var))

	def get_mesure(self,**kwargs):
		output = self.execute(_GET_MESURE_SENSOR_OPCODE, **kwargs)
		ar,av=output.read(INT,INT)
		return ar,av

	def activate(self):
		self.send(_ACTIVATE_SENSORS_OPCODE, BYTE(1))

	def desactivate(self):
		self.send(_DESACTIVATE_SENSORS_OPCODE, BYTE(0))
