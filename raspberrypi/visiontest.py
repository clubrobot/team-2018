from vision import *
from cam2OpenCV import * 
from cubes import *



c = camth()
v = vision(c)
time.sleep(0.5)
v.enable_raw_display()
v.refresh_image()
deb = time.monotonic()
v.calibration()
print(deb - time.monotonic())