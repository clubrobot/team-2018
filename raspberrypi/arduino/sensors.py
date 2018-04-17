#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import math

from common.serialtalks import BYTE, INT, LONG, FLOAT
from common.components import SerialTalksProxy

# Instructions

_GET_MESURE_SENSOR_OPCODE    = 0x10
_ACTIVATE_SENSORS_OPCODE 	 = 0x11
_DESACTIVATE_SENSORS_OPCODE  = 0x12
_GET_NORMAL_OPCODE           = 0x13
_GET_LEFT_SWITCH_OPCODE      = 0x14
_GET_RIGHT_SWITCH_OPCODE     = 0x15

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

	def wait(self,threshold,timeout=2):
		init_time = time.time()
		while (self.get_mesure()[0]<threshold or self.get_mesure()[1]<threshold ) \
			and time.time()-init_time<timeout:
			time.sleep(0.2)

	def activate(self):
		self.send(_ACTIVATE_SENSORS_OPCODE, BYTE(1))

	def desactivate(self):
		self.send(_DESACTIVATE_SENSORS_OPCODE, BYTE(0))

	def get_left_switch(self):
		output = self.execute(_GET_LEFT_SWITCH_OPCODE)
		return bool(output.read(BYTE))
	
	def get_right_switch(self):
		output = self.execute(_GET_RIGHT_SWITCH_OPCODE)
		return bool(output.read(BYTE))