#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import math
from common.serialutils import Deserializer
from common.serialtalks import BYTE, INT, LONG, FLOAT
from common.components import SecureSerialTalksProxy

# Instructions

_GET_MESURE_SENSOR_OPCODE    = 0x10
_ACTIVATE_SENSORS_OPCODE 	 = 0x11
_DESACTIVATE_SENSORS_OPCODE  = 0x12
_GET_NORMAL_OPCODE           = 0x13
_GET_LEFT_SWITCH_OPCODE      = 0x14
_GET_RIGHT_SWITCH_OPCODE     = 0x15



class Sensors(SecureSerialTalksProxy):
	# Default execute result
	_DEFAULT = {_GET_LEFT_SWITCH_OPCODE : Deserializer(BYTE(0)),
				_GET_RIGHT_SWITCH_OPCODE: Deserializer(BYTE(0)),
				_GET_NORMAL_OPCODE      : Deserializer(FLOAT(1000) + FLOAT(0) + FLOAT(1000) + FLOAT(0)),
				_GET_MESURE_SENSOR_OPCODE: Deserializer(INT(1000) + INT(1000))}
	def __init__(self, parent, uuid='sensors'):
		SecureSerialTalksProxy.__init__(self, parent, uuid, Sensors._DEFAULT)

	def get_normal(self,delta_time):
		output = self.execute(_GET_NORMAL_OPCODE,INT(delta_time))
		av_std, av_var, ar_std, ar_var = output.read(FLOAT, FLOAT, FLOAT, FLOAT)
		return ((av_std,av_var),(ar_std,ar_var))

	def get_mesure(self,**kwargs):
		output = self.execute(_GET_MESURE_SENSOR_OPCODE, **kwargs)
		ar,av=output.read(INT,INT)
		if self._compid == "sensorsAr":
			return ar, av
		return ar,av

	def wait(self,threshold,timeout=2):
		init_time = time.time()
		while (self.get_mesure()[0]<threshold or self.get_mesure()[1]<threshold ) \
			and time.time()-init_time<timeout:
			print(self.get_mesure())
			time.sleep(0.2)
		if  not (self.get_mesure()[0]>threshold and self.get_mesure()[1]>threshold ):
			raise TimeoutError()

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
