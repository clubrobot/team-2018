#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
from math import pi


from common.components         import *
from common.serialtalks        import *
from arduino.RobotArm 		   import *


try:
	r = RobotArm()
except:
	print('\'RobotArm\' not connected')
