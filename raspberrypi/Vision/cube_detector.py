
import time

import os, sys, glob
home = os.path.expanduser("~")
for directory in glob.iglob(os.path.join(home, '**/team-2018/raspberrypi'), recursive=True):
	sys.path.append(directory)
	sys.path.append(os.path.join(directory,'common'))
	break
 
from vision import *
from cam2OpenCV import * 
from cubes import *
from gpiodevices import *

side = 0

 

def calibrate(vision, side):
	  vision.calibration()
	  vision.enable()
	  vision.enable_debug()
 
def set_side(s):
	  side = s
  

c = camth()
v = vision(c)
time.sleep(1)
v.refresh_image()

cal_button = Switch(3, calibrate, v, side)
left_button = Switch(5, set_side, LEFT)
right_button = Switch(7, set_side, RIGHT)



while(True):
	v.update()

v.quit()
cal_button.close()
left_button.close()
right_button.close()
