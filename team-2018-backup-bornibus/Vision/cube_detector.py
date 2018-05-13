
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

side ='not'

 

def calibrate(vision):

	  if vision.calibration(side):
	      vision.enable()
	      vision.enable_debug()
 
def set_side(s):
	  global side
	  print(s)
	  side = s
     
def record(camera):
    if camera.record :
        print(" Rec Off")
        camera.record == False
    elif not camera.record : 
        print(" Rec On")
        camera.record == True
    
  

c = camth()
v = vision(c)
time.sleep(1)

cal_button = Switch(3, calibrate, v)
left_button = Switch(5, set_side, 'orange')
right_button = Switch(7, set_side, 'green')
rec_button = Switch(11, record, c)



while(True):
	v.update()

v.quit()
cal_button.close()
left_button.close()
right_button.close()
out.release()
