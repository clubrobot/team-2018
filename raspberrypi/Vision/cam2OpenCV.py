from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import time
import cv2
import numpy as np
import sys


res = (1088,720)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, res)

class camth(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.camera = PiCamera()
		self.camera.resolution = res
		self.camera.framerate = 5
		self.camera.brightness = 60
		self.camera.contrast = 50
		self.rawCapture = PiRGBArray(self.camera, size=res)
		self.image = np.zeros((res[0],res[1],3), np.uint8)
		self.record = False

	def run(self):
          for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
                img = frame.array
                self.image = img.copy()
                
                if self.record : 
                    frame = cv2.flip(img,0)

                      # write the flipped frame
                    out.write(frame)
                self.rawCapture.truncate(0)