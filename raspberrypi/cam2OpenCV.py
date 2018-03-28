from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import time
import cv2
import numpy as np
import sys


class camth(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.camera = PiCamera()
		self.camera.resolution = (800, 608)
		self.camera.framerate = 32
		self.rawCapture = PiRGBArray(self.camera, size=(800, 608))
		self.image = np.zeros((608,800,3), np.uint8)

	def run(self):
          for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
                img = frame.array
                self.image = img.copy()
                self.rawCapture.truncate(0)