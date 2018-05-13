import cv2
import numpy as np
import math


def myadd(x,y):
	 z = []
	 for i in range(len(x)):
		 z.append(x[i]+y[i])
	 return tuple(z)

def mydiv(x,y):
	z=[]
	for i in range(len(x)):
		z.append(x[i] / y)
	return tuple(z)
 
def getNorm(p1, p2):
  return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))

class pilesOfCubes():
	def __init__(self, side):
		x,y,h,s,v = 0, 0, 0, 0, 0
		self.side  = side

		self.blue_cube = (x,y)
		self.yellow_cube = (x,y)
		self.black_cube = (x,y)
		self.green_cube = (x,y)
		self.orange_cube = (x,y)
		
		self.init_blue_cube = (x,y)
		self.init_yellow_cube = (x,y)
		self.init_black_cube = (x,y)
		self.init_green_cube = (x,y)
		self.init_orange_cube = (x,y)

		self.blue_moved = False
		self.black_moved = False
		self.green_moved = False
		self.orange_moved = False
		self.yellow_moved = False
   
		self.error = False
   
		self.coord_min = (200,200)
		self.coord_max = (200,200)
		
		self.hsv_blue = ( (h,s,v ), (h,s,v ))
		self.hsv_black = ( (h,s,v), (h,s,v ))
		self.hsv_yellow = ( (h,s,v), (h,s,v ))
		self.hsv_orange = ((7, 175, 200),(9, 187, 210))
		self.hsv_green = ( (h,s,v), (h,s,v ))
			
		self.mat = np.float32([[  6.34119160e-01 , 1.78735109e-02 , -1.61388226e+00], \
 					                [ -2.48795277e-02 , 9.66831621e-01, -3.04253049e+01], \
 					                [ -1.26940623e-03 , 4.06277788e-03,  1.00000000e+00]]) 
      
		self.image = np.zeros((200,200,3), np.uint8)
		self.hsv_image = np.zeros((608,800,3), np.uint8)
		self.first_cube_corners = ((x,y) ,(x,y) ,(x,y) ,(x,y))

		self.square_ker_op = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
		self.square_ker_cls  = cv2.getStructuringElement(cv2.MORPH_RECT,(13,13))
		
		self.color = ['blue', 'black', 'orange', 'green', 'yellow']

	def init(self, img):
		self.refresh_image(img)
		self.find_corner()
		if not self.error :
			self.sort_corner()
			self.init_cube_center_arbitrary()
			self.init_hsv_tresh()
			for c in self.color: 
				self.init_cube_center(c)
		
		
	def convert2hsv(self):
		self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

	def init_hsv_tresh(self):
		for c in self.color: 
			hsv_min, hsv_max = self.hsv_treshold_finder(c)
			self.set_hsv_tresh(c, hsv_min, hsv_max)
   
	def set_mat(self, m):
		self.mat = np.copy(m)
   		
	def hsv_treshold_finder(self, color):
		if(color == 'blue'):
			cube_min = (self.init_blue_cube[0] - 4 , self.init_blue_cube[1] - 4 )
			cube_max = (self.init_blue_cube[0] + 4 , self.init_blue_cube[1] + 4 )
		elif(color == 'yellow'):
			cube_min = (self.init_yellow_cube[0] - 4 , self.init_yellow_cube[1] - 4 )
			cube_max = (self.init_yellow_cube[0] + 4 , self.init_yellow_cube[1] + 4 )
		elif(color == 'black'):
			cube_min = (self.init_black_cube[0] - 4 , self.init_black_cube[1] - 4 )
			cube_max = (self.init_black_cube[0] + 4 , self.init_black_cube[1] + 4 )
		elif(color == 'green'):
			cube_min = (self.init_green_cube[0] - 4 , self.init_green_cube[1] - 4 )
			cube_max = (self.init_green_cube[0] + 4 , self.init_green_cube[1] + 4 )
		elif(color == 'orange'):
			cube_min = (self.init_orange_cube[0] - 4 , self.init_orange_cube[1] - 4 )
			cube_max = (self.init_orange_cube[0] + 4 , self.init_orange_cube[1] + 4 )

		hsv_min = [180,255,255]
		hsv_max = [0,0,0]
   
		for row in range(cube_min[0], cube_max[0]):
			for col in range(cube_min[1], cube_max[1]):
				h, s, v = self.hsv_image[col, row]
		  
				if h > hsv_max[0]:
					hsv_max[0] = h
				if h < hsv_min[0]:
					hsv_min[0] = h
 			  
				if s > hsv_max[1]:
					hsv_max[1] = s
				if s < hsv_min[1]:
					hsv_min[1] = s
					
				if v > hsv_max[2]:
					hsv_max[2] = v
				if v < hsv_min[2]:
					hsv_min[2] = v
				 
		hsv_min[2] -= 40
		hsv_max[2] += 40
  
		hsv_min[1] -= 40
		hsv_max[1] += 40
   
		hsv_min[0] -= 2
		hsv_max[0] += 2
   
		return (tuple(hsv_min), tuple(hsv_max))
	
	
	def init_cube_center_arbitrary(self):
		moy_x = 0
		moy_y = 0
		for i in self.first_cube_corners : 
			x,y = i
			moy_x += x 
			moy_y += y 
		moy_x = int(moy_x / 4)
		moy_y = int(moy_y / 4)
		
		self.init_yellow_cube = (moy_x, moy_y)
		self.init_blue_cube = (moy_x, moy_y-16)
		self.init_black_cube = (moy_x, moy_y+16)
		self.init_green_cube = (moy_x + self.side*16, moy_y)
		self.init_orange_cube = (moy_x - self.side*16, moy_y)

	def init_cube_center(self, color): 
		if(color == 'blue'):
			hsv_min, hsv_max = self.hsv_blue
			self.init_blue_cube = self.gravitycenter_search(hsv_min, hsv_max)
		elif(color == 'yellow'):
			hsv_min, hsv_max = self.hsv_yellow
			self.init_yellow_cube = self.gravitycenter_search(hsv_min, hsv_max)
		elif(color == 'black'):
			hsv_min, hsv_max = self.hsv_black
			self.init_black_cube = self.gravitycenter_search(hsv_min, hsv_max)
		elif(color == 'green'):
			hsv_min, hsv_max = self.hsv_green
			self.init_green_cube = self.gravitycenter_search(hsv_min, hsv_max)
		elif(color == 'orange'):
			hsv_min, hsv_max = self.hsv_orange
			self.init_orange_cube = self.gravitycenter_search(hsv_min, hsv_max)



	def save_img(self):
		cv2.imwrite('image.jpg', self.image)
	
	def display_img(self, window_name): 
		cv2.imshow(window_name, self.image)
		cv2.waitKey(1)
		
	def display_cube(self, color, window_name): 
		hsv_min, hsv_max = self.get_hsv_tresh(color)

		min_array = np.array([hsv_min[0],hsv_min[1],hsv_min[2]])
		max_array = np.array([hsv_max[0],hsv_max[1],hsv_max[2]])
		gray =  cv2.inRange(self.hsv_image, min_array, max_array)
		gray = self.filtrage(gray)
		mask_inv = cv2.bitwise_not(gray)

		res = cv2.bitwise_and(self.image,self.image,mask = mask_inv)
		cv2.imshow(window_name + "  "+color, res )
		cv2.waitKey(1)		

	def set_coords(self, min, max):
		
		self.coord_min = min
		self.coord_max = max
		self.set_region((max[0] - min[0]), (max[1] - min[1]))
	
	def get_coord(self):
		return (self.coord_min, self.coord_max)

	def perspective_remover(self):
		self.image = cv2.warpPerspective(self.image, self.mat,(100,100))
		self.set_region(100, 100)
		
	def sort_corner(self):
		moy_x = 0 
		moy_y = 0
		for i in self.first_cube_corners : 
			moy_x += i[0]
			moy_y += i[1]
		moy_x, moy_y = (round(moy_x/4) ,round(moy_y/4))
		
		f_right = False
		f_left = False
		f_up = False
		f_down = False
		sorted_corner = [(0,0),(0,0),(0,0),(0,0)]
		for i in self.first_cube_corners : 
			if(i[0] <= moy_x):
				f_left = True
			if(i[0] > moy_x):
				f_right = True			
			if(i[1] <= moy_y):
				f_up = True			
			if(i[1] > moy_y):
				f_down = True
			
			if(f_left and f_up):
				sorted_corner[0] = i 
			if(f_right and f_up):
				sorted_corner[1] = i 
			if(f_right and f_down):
				sorted_corner[2] = i
			if(f_left and f_down):
				sorted_corner[3] = i

			f_right = False
			f_left = False
			f_up = False
			f_down = False
			
		self.first_cube_corners = tuple(sorted_corner)

	def display_corner(self):
		image2 = np.copy(self.image)
		for i in self.first_cube_corners:
			x,y = i
			cv2.circle(image2,(x,y),3,255,-1)

		cv2.imshow('image', image2)

	def filtrage(self, img):
		
		img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, self.square_ker_cls)
		return img

	def gravitycenter_search(self, hsv_min, hsv_max):
		width = self.region_shape[0]
		height = self.region_shape[1]
		
		p = 0
		x_sum = 0 
		y_sum = 0
		
   
		min_array = np.array([hsv_min[0],hsv_min[1],hsv_min[2]])
		max_array = np.array([hsv_max[0],hsv_max[1],hsv_max[2]])
		gray =  cv2.inRange(self.hsv_image, min_array, max_array)
		
		gray = self.filtrage(gray)
		
		for x in range(width):
			for y in range(height):
				
				pi = gray[y,x]
				if(pi>250):
					p += pi
					x_sum += x*pi  
					y_sum += y*pi
		if(p != 0):
			xg = x_sum/p
			yg = y_sum/p
		else:
			xg = -1
			yg = -1
		pos = (round(xg), round(yg))
		return pos

	def set_region(self, w, h): 
		self.region_shape = (w, h)
						  
						  		  			  
	def is_moved(self): 
		return self.blue_moved or self.black_moved or self.green_moved or self.orange_moved or self.yellow_moved
			   
			   			  		
	def is_color_moved(self, color):
		if(color == 'blue'):
			return self.blue_moved
		elif(color == 'yellow'):
			return self.yellow_moved
		elif(color == 'black'):
			return self.black_moved
		elif(color == 'green'):
			return self.green_moved
		elif(color == 'orange'):
			return self.orange_moved
	  
	def set_color_moved(self, color, moved):
		if(color == 'blue'):
			self.blue_moved = moved
		elif(color == 'yellow'):
			self.yellow_moved = moved
		elif(color == 'black'):
			self.black_moved = moved
		elif(color == 'green'):
			self.green_moved = moved
		elif(color == 'orange'):
			self.orange_moved = moved
	
	
	def refresh_image(self, img):
		self.image = img[self.coord_min[1]: self.coord_max[1], self.coord_min[0]: self.coord_max[0]].copy()
		self.perspective_remover()
		self.convert2hsv()

	def find_corner(self):
		gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
   
		corners = cv2.goodFeaturesToTrack(gray,20,0.01,10)
		try:
			corners = np.int0(corners)

			center = (round(self.region_shape[0] / 2) , round(self.region_shape[1] /2) )
			a = self.region_shape[0]*self.region_shape[1]
			best = []
			norm_min = a
			x = (a,a)
			c = []
			for i in corners: 
				x,y = i.ravel()
				c.append((x,y))
  
			for b in range(4):
				for i in c : 
					x,y = i
					norm_i = math.pow((x - center[0]), 2) + math.pow((y - center[1]), 2)
					if norm_i < norm_min : 
					  norm_min = norm_i
					  z = i
				best.append(z)
				del(c[c.index(z)])
				norm_min = a
  
			self.first_cube_corners = tuple(best)
	
		except TypeError:
			self.error = True

	
	def set_cube_position(self, color, pos_xy):
			if(color == 'blue'):
				self.blue_cube = pos_xy
			elif(color == 'yellow'):
				self.yellow_cube = pos_xy
			elif(color == 'black'):
				self.black_cube = pos_xy
			elif(color == 'green'):
				self.green_cube = pos_xy
			elif(color == 'orange'):
				self.orange_cube = pos_xy
	
	def get_init_cube_position(self, color):
			if(color == 'blue'):
				return self.init_blue_cube
			elif(color == 'yellow'):
				return self.init_yellow_cube
			elif(color == 'black'):
				return self.init_black_cube
			elif(color == 'green'):
				return self.init_green_cube
			elif(color == 'orange'):
				return self.init_orange_cube

	def set_hsv_tresh(self, color, min, max):
			if(color == 'blue'):
				self.hsv_blue = (min, max)
			elif(color == 'yellow'):
				self.hsv_yellow = (min, max)
			elif(color == 'black'):
				self.hsv_black = (min, max)
			elif(color == 'green'):
				self.hsv_green = (min, max)
			elif(color == 'orange'):
				self.hsv_orange = (min, max)

	def get_hsv_tresh(self, color):
			if(color == 'blue'):
				return self.hsv_blue
			elif(color == 'yellow'):
				return self.hsv_yellow
			elif(color == 'black' ):
				return self.hsv_black
			elif(color == 'green'):
				return self.hsv_green
			elif(color == 'orange'):
				return self.hsv_orange

	def update_pile_position(self): 
		for c in self.color : 
			self.update_cube_position(c)

	def update_cube_position(self, color):
		hsv_min, hsv_max = self.get_hsv_tresh(color)
	
		pos_xy = self.gravitycenter_search(hsv_min, hsv_max)
		self.set_cube_position(color, pos_xy)
	
		norm = getNorm(self.get_init_cube_position(color), self.get_cube_position(color))
		flag = norm >=10
	
		self.set_color_moved(color, flag)


	def get_cube_position(self, color):
		if(color == 'blue'):
			return self.blue_cube
		elif(color == 'yellow'):
			return self.yellow_cube
		elif(color == 'black'):
			return self.black_cube
		elif(color == 'green'):
			return self.green_cube
		elif(color == 'orange'):
			return self.orange_cube

	def cube_corner_checker(self):
		min_x, min_y = self.first_cube_corners[0], 
		max_x, max_y  = self.first_cube_corners[0]
		
		for corn in self.first_cube_corners: 
			if corn[0] < min_x : 
				min_x = corn[0]
			elif corn[0] > max_x : 
				min_x = corn[0]
			if corn[1] > max_y : 
				min_y = corn[1]
			elif corn[1] > max_y : 
				min_y = corn[1]

			area = (max_x - min_x)(max_y - min_y)

			return area > 200 and area < 350
