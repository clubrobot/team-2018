#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
from math import pi


from common.components         import *
from common.serialtalks        import *
from arduino.RobotArm 		   import *

hostname = ""
if hostname=="":
	print ("IP adress :  ")
	hostname=input()	
	if(len(hostname.split("."))==1 and len(hostname)>0):
		hostname="192.168.1."+hostname
	print ("Try reaching raspberry at IP "+hostname+"...")


try:
	m = Manager(hostname)
	m.connect(10)
except:
	raise
	m = Manager()
	m.connect(10)

try:
	r = RobotArm(m)
except:
	print('\'RobotArm\' not connected')
