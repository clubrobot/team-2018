#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Common import

import time
from math import pi

# Add the robot directory to the import path

import os, sys
sys.path.append("../../common/")
sys.path.append("..")

# Check for the Rapsberry Pi address
# It looks for a file in the current directory, whose name is
# a valid IP address

hostname = ""
if hostname=="":
	print ("IP adress :  ")
	hostname=input()
	if(len(hostname.split("."))==1):
		hostname="192.168.1."+hostname
	print ("Try reaching raspberry at IP "+hostname+"...")
# Import robot stuff
#from common.modulesrouter      import *
from components         import *
#from common.serialtalks        import *
#from secondaryrobot.modules    import *
from wheeledbase        import *
from waterlauncher      import *
from watersorter        import *
from display            import *
from sensors            import *

# Define temporary modules

# Connect to the Raspberry Pi and the different modules

try:
	m = Manager(hostname)
	m.connect(10)
except:
	raise
	m = Manager()
	m.connect(10)

try:
	b = WheeledBase(m)
except :
	print('\'wheeledbase\' not connected')

try:
    d = WaterSorter(m)
    l = WaterLauncher(m)
except :
	print('\'wattershooter\' not connected')

try:
#	l = Module(m, 'display')
	ssd = SevenSegments(m)
	led1 = LEDMatrix(m, 1)
	led2 = LEDMatrix(m, 2)
except:
	print('\'display\' not connected')

try:
	s = Sensors(m)
except :
	print('\'sensors\' not connected')


#rb = LightButtonModule(m, 15, 16)
#bb = LightButtonModule(m, 23, 24)
#yb = LightButtonModule(m, 35, 36)
#gb = LightButtonModule(m, 21, 22)
#sw = SwitchModule(m, 29)
