import numpy as np 
import matplotlib.pyplot as plt
from setup_bornibus import *
from time           import sleep
TIME = 20
TIME_STEP = 0.01
STEP = TIME/TIME_STEP
print(STEP)
red = np.array([[]])

def add_red_value(value):
    global red
    red = np.c_[red,value]

green = np.array([[]])

def add_green_value(value):
    global green
    green = np.c_[green,value]

blue = np.array([[]])

def add_blue_value(value):
    global blue
    blue = np.c_[blue,value]

input("Press to begin !")
x = np.arange(0., TIME, TIME_STEP)
for i in range(int(STEP)):
    print(i)
    red_val, green_val, blue_val = d.get_water_color()
    add_red_value(red_val)
    add_green_value(green_val)
    add_blue_value(blue_val)
    sleep(TIME_STEP)

plt.plot(x,red[0],'r--',x,green[0],'g--',x,blue[0],'b--')
plt.axis([0, TIME,0, np.amax([red[0],green[0],blue[0]])])
plt.show()
