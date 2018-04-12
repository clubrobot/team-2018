import time
import cv2
import numpy as np
import sys
import math
from cubes import *


LEFT = -1
RIGHT = +1

M_rd = np.float32([[  6.34119160e-01 , 1.78735109e-02 , -1.61388226e+00], \
 					[ -2.48795277e-02 , 9.66831621e-01, -3.04253049e+01], \
 					[ -1.26940623e-03 , 4.06277788e-03,  1.00000000e+00]])

M_rm = np.float32([[  1.41047797e+00 , -2.30794243e-01, -1.76176546e+01], \
 					[ -7.63566098e-01  ,  3.43790512e+00  ,-1.65996162e+02],\
 					[ -1.10545487e-02  , 2.12873134e-02 ,  1.00000000e+00]])

M_ru = np.float32([[  3.69230769e+00  , 1.00000000e+00 , -2.25076923e+02],\
 					[ -5.47339951e-14  , 8.38461538e+00 , -5.94307692e+02],\
 					[ -1.10046521e-15  , 3.84615385e-02  , 1.00000000e+00]])


M_ld = np.float32([[  9.15331808e-01 ,  3.89016018e-01 , -6.98169336e+01],\
 					[ -8.82627305e-15 , 9.01601831e-01 , -2.88832952e+01],\
 					[ -1.74773390e-16  , 2.28832952e-03 , 1.00000000e+00]])


M_lm = np.float32([[  7.03640197e-01 ,  4.81206492e-01 , -8.10514235e+01],\
 		   			[ -8.44458274e-02 ,  8.09575669e-01 , -4.09903839e+01],\
 			   		[ -3.63291504e-03 , -1.91990043e-04 ,  1.00000000e+00]])

M_lu = np.float32([[  8.60986547e-01  , 3.58744395e-01 , -7.09327354e+01],\
 		  			[  7.17488789e-02 ,  1.36322870e+00 , -9.27443946e+01],\
 			   		[  1.26634814e-16 ,  1.30971622e-16 ,  1.00000000e+00]])

coords_rd = ((711, 507),(911, 707))  
coords_rm = ((817, 285), (1017, 485))
coords_ru = ((526, 208), (726, 408))

coords_ld = ((55, 516), (255, 716))
coords_lm = ((0, 320), ( 200, 520))
coords_lu = ((247,224), (447,424))

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
	
		  self.piles_names = ('lu', 'lm', 'ld', 'ru', 'rm', 'rd')
		  self.color = ('blue', 'green', 'orange', 'yellow', 'black')
		  self.piles = [self.lu_pile , self.lm_pile, self.ld_pile, self.ru_pile, self.rm_pile, self.rd_pile]
		  self.enabled = False
	
		  self.timestep = 1
		  self.precedentTime = 0
		  
		  self.raw_image = self.camera.image.copy()
		  
		  self.display = False
		  self.piles_showing = [False , False, False, False, False, False]
		  self.colors_showing = [False , False, False, False, False]
		  self.full_image_showing = False
		  self.debug = False
		  

	  def enable_display(self):
		  self.display = True
		  
	  def disable_display(self):
		  self.display = False
	
	  def stop_cam(self):
		  self.camera.stop
		  
	  def display_image(self):
		  cv2.imshow('Terrain', self.raw_image)
		  cv2.waitKey(1)
			  
 
	  def show_pile(self, names, colors):
		  if names == 'all':
			  self.piles_showing = [True , True, True, True, True, True]
		  else: 
			  self.piles_showing[self.piles_names.index(names)] = True
		  if colors == 'all':
			  self.colors_showing = [True , True, True, True, True]
		  else:
			  self.colors_showing[self.color.index(colors)] = True 
		  
	  def display_selection(self):
		  for i in range(6):
			  for c in range(5):
				  if(self.piles_showing[i] and self.colors_showing[c]):
					  self.piles[i].display_cube(self.color[c], self.piles_names[i])
		  if self.full_image_showing :
		  	   self.display_image()
	  
	  def clear_selection(self):
		  self.piles_showing = [False , False, False, False, False, False]
		  self.colors_showing = [False , False, False, False, False, False]
		  self.full_image_showing = False	
	
	
	  def show_image(self):
		  self.full_image_showing = True
	  
	  def refresh_image(self):
		  self.raw_image = self.camera.image.copy()
		  for p in self.piles:
					p.refresh_image(self.raw_image)
		  return self.raw_image
	 
	  def calibration(self):
		  self.refresh_image()
		  for p in self.piles:
					p.init(self.raw_image)
		  self.ld_pile.init(self.raw_image)
		  print(self.ld_pile.hsv_blue)
		  print(self.ld_pile.hsv_orange)
		  print(self.ld_pile.hsv_yellow)
		  print(self.ld_pile.hsv_black)
		  print(self.ld_pile.hsv_green)
	
	  def check_position(self): 
		  for p in self.piles: 
					p.update_pile_position()
		  self.ld_pile.update_pile_position()
	
	  def process(self):
		  self.check_position()
		  if self.debug :
			  self.debug_printing()	  					   
								   				   					   				  											   			   
		  if(self.display):   	            
			  self.display_selection()
			  key = cv2.waitKey(100) & 0xFF 
			  if key == ord("q"):
				  self.clear_selection()
				  cv2.destroyAllWindows()  
	
	  def enable(self):
		  self.enabled = True
	  def disable(self):
		  self.enabled = False
	
	  def setTimestep(self, timestep):   
		  self.timestep = timestep 

	  def save_raw_image(self):
		  cv2.imwrite('terrain.jpg', self.raw_image)
		  							   
	  def enable_debug(self):
		  self.debug = True	
	  
	  def disable_debug(self):
		  self.debug = False							   				   		  		 	   					   				   

	  def update(self):
		  self.refresh_image()
		  if (self.enabled and (time.monotonic() - self.precedentTime )> self.timestep):
			  self.precedentTime = time.monotonic()
			  self.process()
				  
	  def debug_printing(self):
		   for i in range(6):

			   if( not self.piles[i].is_moved()):
				   print(self.piles_names[i] + " : Ok")
			   else:
				   lign = self.piles_names[i] + " ->   " 
				   for c in self.color:
					   if self.piles[i].is_color_moved(c):
						   lign += c + " :  MOVED   " 
					   else:
						   lign += c + " : Ok "
				   print(lign)
		   print("\n **---------------** \n")
					  
				  
				
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