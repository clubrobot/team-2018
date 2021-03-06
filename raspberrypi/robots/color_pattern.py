import cv2 as cv
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import math
 
def getNorm(p1, p2):
  return round(math.sqrt(math.pow((int(p1[0]) - int(p2[0])), 2) + math.pow((int(p1[1]) - int(p2[1])), 2) + math.pow((int(p1[2]) - int(p2[2])), 2)))

def mydiv(x,y):
    z=[]
    for i in range(len(x)):
        z.append(round(x[i] / y))
    return tuple(z)

#colors_constants = { 'orange': ( 250, 133, 38), 'blue' : ( 51, 131, 154), 'yellow' : ( 253, 238, 0), 'black': ( 0, 0, 0), 'green': ( 80, 182, 20), 'grey': (193, 212, 136)}
colors_constants = { 'orange': ( 217, 114, 60), 'blue' : ( 11, 92, 138), 'yellow' : ( 245, 180, 42), 'black': ( 0, 0, 0), 'green': ( 99, 152, 65), 'grey': (193, 212, 136)}

class Pattern:
    ORANGE = 0
    BLACK = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4

    code = {"orange:": ORANGE, "black": BLACK, "green": GREEN, "yellow": YELLOW, "blue": BLUE}
    def __init__(self):
        self.color_pat = ["unknown", "unknown", "unknown"]

        self.image = np.zeros((200,200,3), np.uint8)

        #setting up the camera
        self.camera = PiCamera()
        self.camera.resolution = (1088,720)
        self.camera.brightness = 60
        self.camera.contrast = 50

        #initialize a first image
        self.rawCapture=PiRGBArray(self.camera)
        self.camera.capture(self.rawCapture,format='bgr')
        self.image=self.rawCapture.array.copy()
        self.rawCapture.truncate(0)


    def find_pattern(self):
        height = round(self.image.shape[0]/2) + 20
        lowerlim = round(self.image.shape[1]/4)
        upperlim = round(3*self.image.shape[1]/4)


        i = lowerlim
        color = self.image[height, i]
        colorList = []
        newcolor = []
        while(i<upperlim):
            prec = color
            sum = [0,0,0]
            for j in range(height -5, height + 5):
                color = self.image[j, i]
                sum = [sum[0] + color[0] , sum[1]+color[1] , sum[2]+color[2]]
            color = mydiv(sum, 10)

            i +=20
            norm = getNorm(color, prec)
            if norm > 80 :
                colorList.append(newcolor)
                newcolor = []
            else :
                newcolor.append(color)
        colorList.append(newcolor)

        moy = []
        for list in colorList:
            sum = [0,0,0]
            n = 0

            for color in list:
                sum = [sum[0] + color[0] , sum[1]+color[1] , sum[2]+color[2]]
                n +=1
            if n !=0:
                moy.append(mydiv(sum, n))

        print(moy)


        color_number = 0
        for c in moy :
            RGB_color = (c[2], c[1], c[0])
            min = 1000000000000
            self.color_pat[color_number] = self.color_guesser(RGB_color)
            if self.color_pat[color_number] != 'grey' :
                color_number +=1
            if color_number >2 :
                break

    def get_pattern(self):
        return self.color_pat

    def get_pattern_encoded(self):
        return [Pattern.code[color] for color in self.color_pat]

    def color_guesser(self, rgb):
        name = "unknown"
        for color_name, color_value in colors_constants.items():
            norm = getNorm(rgb, color_value)
            if norm <= min :
                min = norm
                name = color_name
        return name


    def take_photo(self):
        self.camera.capture(self.rawCapture,format='bgr')
        self.image=self.rawCapture.array.copy()
        self.rawCapture.truncate(0)

    def save_pattern(self):
        cv.imwrite('pattern.jpg', self.image)

