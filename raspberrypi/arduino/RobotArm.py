#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import math

from common.serialtalks import BYTE, INT, LONG, FLOAT, SerialTalks
#from common.components import SerialTalksProxy


_BEGIN_OPCODE 		 = 0X11
_SET_POS_OPCODE 	 = 0X12

_SET_X_OPCODE 		 = 0X13
_SET_Y_OPCODE 		 = 0X14
_SET_Z_OPCODE 		 = 0X15
_SET_THETA_OPCODE 	 = 0X16
_SET_SPEED_OPCODE 	 = 0X17

_GET_POS_OPCODE 	 = 0X18
_GET_POS_THEO_OPCODE = 0X19
_SET_ANGLES_OPCODE	 = 0X1A

_OPEN_GRIPPER_OPCODE = 0X1B
_CLOSE_GRIPPER_OPCODE = 0X1C

class RobotArm(SerialTalks):	
	def __init__(self, uuid='ttyUSB0'):
		SerialTalks.__init__(self, "/dev/{}".format(uuid))

	def begin(self):
		self.send(_BEGIN_OPCODE)

	def set_pos(self, x, y ,z ,theta):
		self.send(_SET_POS_OPCODE, FLOAT(x), FLOAT(y), FLOAT(z), FLOAT(theta))

	def set_x(self,x):
		self.send(_SET_X_OPCODE, FLOAT(x))

	def set_y(self,y):
		self.send(_SET_Y_OPCODE, FLOAT(y))

	def set_z(self,z):
		self.send(_SET_Z_OPCODE, FLOAT(z))

	def set_theta(self,theta):
		self.send(_SET_THETA_OPCODE, FLOAT(theta))

	def set_speed(self,speed):
		self.send(_SET_THETA_OPCODE, FLOAT(speed))

	def get_pos(self):
		output = self.execute(_GET_POS_OPCODE)
		x, y, z = output.read(FLOAT, FLOAT, FLOAT)
		return (x,y,z)

	def get_pos_theo(self):
		output = self.execute(_GET_POS_THEO_OPCODE)
		x, y, z = output.read(FLOAT, FLOAT, FLOAT)
		return (x,y,z)

	def set_angles(self,a,b,c):
		self.send(_SET_ANGLES_OPCODE, FLOAT(a),FLOAT(b),FLOAT(C))

	def open_gripper(self):
		self.send(_OPEN_GRIPPER_OPCODE)

	def close_gripper(self):
		self.send(_CLOSE_GRIPPER_OPCODE)	