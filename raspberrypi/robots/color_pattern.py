import cv3 as cv
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
 

class Pattern:
	def __init__(self):
		self.first_color = "unknown"
		self.middle_color = "unknown"
		self.last_color = "unknown"
		
		#setting up the camera
		self.camera = PiCamera()
		self.camera.resolution = (1088,720)
		self.camera.brightness = 60
		self.camera.contrast = 50
		
		#initialize a first image
		self.rawCapture=PiRGBArray(self.camera)
		self.camera.capture(self.rawCapture,format='bgr')
		self.image=rawCapture.array.copy()
		self.rawCapture.truncate(0)
	
	def find_pattern(self, image):
		a=1


	def get_pattern(self):
		a=1

	def color_guesser(self, r, g, b):
		a=1


	def take_photo(self):
		self.camera.capture(self.rawCapture,format='bgr')
		self.image=rawCapture.array.copy()
		self.rawCapture.truncate(0)

	def save_pattern(self):
		cv.imwrite('pattern.jpg', self.image)
