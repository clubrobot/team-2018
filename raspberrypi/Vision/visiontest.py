from vision import *
from cam2OpenCV import * 
from cubes import *
import time

deb = time.monotonic()

c = camth()
v = vision(c)
time.sleep(1)
v.refresh_image()

v.enable_display()
v.show_image()
v.enable_debug()
v.show_pile('ld', 'all')
v.enable()

v.calibration()

print(deb - time.monotonic())
while(True):
   v.update()
