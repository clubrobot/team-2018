import cv2
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


	def get_pattern(self):

	def color_guesser(self, r, g, b):


	def take_photo(self):
		self.camera.capture(self.rawCapture,format='bgr')
		self.image=rawCapture.array.copy()
		self.rawCapture.truncate(0)

	def save_pattern(self):
		cv2.imwrite('pattern.jpg', self.image)
