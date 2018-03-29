import time
import cv2
import numpy as np
import sys
import math
from cubes import *


LEFT = -1
RIGHT = +1

M_rd = np.float32([[  8.04199656e-01 ,  5.36014200e-02 , -2.05420916e+01], \
				  [ -1.09929542e-02 ,  6.64995877e-01 ,  6.56306263e+00], \
				  [  8.20750763e-04 ,  2.38242688e-03  , 1.00000000e+00]])

M_rm = np.float32([[  8.04199656e-01 ,  5.36014200e-02 , -2.05420916e+01], \
				  [ -1.09929542e-02 ,  6.64995877e-01 ,  6.56306263e+00], \
				  [  8.20750763e-04 ,  2.38242688e-03  , 1.00000000e+00]])

M_ru= np.float32([[  8.04199656e-01 ,  5.36014200e-02 , -2.05420916e+01], \
				  [ -1.09929542e-02 ,  6.64995877e-01 ,  6.56306263e+00], \
				  [  8.20750763e-04 ,  2.38242688e-03  , 1.00000000e+00]])
 
M_ld = np.float32([[  7.42305926e-01 , 1.13918236e-01 , 4.96463023e+00], \
 					[ -3.60128617e-01 , 1.10610932e+00 , 1.03665595e+01], \
					[ -4.59347726e-03 , 4.13412954e-03 , 1.00000000e+00]])


M_lm = np.float32([[  8.04199656e-01 ,  5.36014200e-02 , -2.05420916e+01], \
				  [ -1.09929542e-02 ,  6.64995877e-01 ,  6.56306263e+00], \
				  [  8.20750763e-04 ,  2.38242688e-03  , 1.00000000e+00]])

M_lu = np.float32([[  8.04199656e-01 ,  5.36014200e-02 , -2.05420916e+01], \
				  [ -1.09929542e-02 ,  6.64995877e-01 ,  6.56306263e+00], \
				  [  8.20750763e-04 ,  2.38242688e-03  , 1.00000000e+00]])

coords_lu = ( ( 200, 200 ), ( 300, 300 ) )
coords_lm = ( ( 200, 200 ), ( 300, 300 ) )
coords_ld = ( ( 200, 200 ), ( 300, 300 ) )
coords_ru = ( ( 200, 200 ), ( 300, 300 ) )
coords_rm = ( ( 200, 200 ), ( 300, 300 ) )
coords_rd = ( ( 200, 200 ), ( 300, 300 ) )

class vision():

      def __init__(self, cam):
          cam.start()
          self.camera = cam
    
          self.lu_pile = pilesOfCubes(M_lu, LEFT, coords_lu[0], coords_lu[1])
          self.lm_pile = pilesOfCubes(M_lm, LEFT, coords_lm[0], coords_lm[1]) 
          self.ld_pile = pilesOfCubes(M_ld, LEFT, coords_ld[0], coords_ld[1])
          self.ru_pile = pilesOfCubes(M_ru, RIGHT, coords_ru[0], coords_ru[1])
          self.rm_pile = pilesOfCubes(M_rm, RIGHT, coords_rm[0], coords_rm[1])
          self.rd_pile = pilesOfCubes(M_rd, RIGHT, coords_rd[0], coords_rd[1])
    
          self.piles = [self.lu_pile , self.lm_pile, self.ld_pile, self.ru_pile, self.rm_pile, self.rd_pile]
    		
          self.enabled = False
    
          self.timestep = 1
          self.precedentTime = 0
          
          self.raw_image = self.camera.image.copy()
          self.raw_display = False

      def enable_raw_display(self):
          self.raw_display = True
	
      def stop_cam(self):
          self.camera.stop

      def refresh_image(self):
          self.raw_image = self.camera.image.copy()
          for p in self.piles:
			        p.refresh_image(self.raw_image)
          return self.raw_image
	 
      def calibration(self):
          self.refresh_image()
          for p in self.piles:
              p.init(self.raw_image)
	
      def check_position(self): 
          for p in self.piles: 
              p.update_pile_position()
	
      def process(self):
          self.refresh_image()
          for p in self.piles: 
              p.refresh_image(self.raw_image)
              p.update_pile_position()
	
      def enable(self):
          self.enabled = True
      def disable(self):
          self.enabled = False
	
      def setTimestep(self, timestep):   
          self.timestep = timestep 

      def save_raw_image(self):
          cv2.imwrite('terrain.jpg', self.raw_image)

      def update(self):
          self.refresh_image()
          if (self.enabled and time.monotonic() - self.precedentTime > self.timestep):
              self.precedentTime = time.monotonic()
              self.process()
              return True

          if(self.raw_display):
              cv2.imshow('Raw_image', self.raw_image)
              key2 = cv2.waitKey(1) & 0xFF               
              if key2 == ord("q"):
                    self.raw_display = False
                    cv2.destroyAllWindows()
          return False

      def isEnabled(self): 
          return self.enabled

      def getTimestep(self): 
          return self.timestep
    

def edge_finder(gravitycenter, n=1):
		global gray
		global img
		lim = []
		i = 0
		while i<math.radians(360) :
			cos = math.cos(i)
			sin = math.sin(i)
			l = 0
			border = False
			while l < 100 and (not border):
				l+=1
				x = int( gravitycenter[0] + l * cos)
				y = int(gravitycenter[1] + l * sin)
				border = (gray[y, x] < 10)
			if border :
				lim.append((x, y))
			
			i += math.radians(360/(n*4))

		return tuple(lim)