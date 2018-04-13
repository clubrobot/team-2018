import time
import cv2
import numpy as np
import sys
import math
from cubes import *
from constants import * 


class vision():

	  def __init__(self, cam):
		  cam.start()
		  self.camera = cam
	
		  self.lu_pile = pilesOfCubes(LEFT)
		  self.lm_pile = pilesOfCubes(LEFT) 
		  self.ld_pile = pilesOfCubes(LEFT)
		  self.ru_pile = pilesOfCubes(RIGHT)
		  self.rm_pile = pilesOfCubes(RIGHT)
		  self.rd_pile = pilesOfCubes(RIGHT)
	
		  self.piles_names = ('rd', 'rm', 'ru', 'ld', 'lm', 'lu')
		  self.color = ('blue', 'green', 'orange', 'yellow', 'black')
		  self.piles = [self.rd_pile, self.rm_pile, self.ru_pile, self.ld_pile , self.lm_pile, self.lu_pile]
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
	 
	  def calibration(self, side):
		  self.raw_image = self.camera.image.copy()   
		  if side == 'orange':
			  for i in range(6):
				  self.piles[i].set_mat(O_Mtx[i])
				  self.piles[i].set_coords(O_coords[i][0], O_coords[i][1])                                   
				  self.piles[i].init(self.raw_image)

		  elif side == 'green':
			  for i in range(6):
				  self.piles[i].set_mat(G_Mtx[i])
				  self.piles[i].set_coords(G_coords[i][0], G_coords[i][1])                                   
				  self.piles[i].init(self.raw_image)
		  else:
			  print("not a Color")
		  
												   
	
	  def check_position(self): 
		  for p in self.piles: 
					p.update_pile_position()
	
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
		  
		   if (self.enabled and (time.monotonic() - self.precedentTime )> self.timestep):
			   self.refresh_image()
			   self.process()
			   self.precedentTime = time.monotonic()
			  
				  
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