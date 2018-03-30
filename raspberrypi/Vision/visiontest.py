from vision import *
from cam2OpenCV import * 
from cubes import *
import time



c = camth()
v = vision(c)
time.sleep(1)
v.refresh_image()

#v.enable_display()
v.show_image()
v.enable_debug()
v.show_pile('all', 'all')
v.enable()
deb = time.monotonic()
v.calibration()

print(deb - time.monotonic())
while(True):
   v.update()
