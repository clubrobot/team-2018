#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.roadmap import RoadMap
from common.geogebra import Geogebra
# Check for the Rapsberry Pi address
# It looks for a file in the current directory, whose name is
# a valid IP address


# Import robot stuff

from common.components import *
from arduino.wheeledbase import *
from arduino.waterlauncher import *
from arduino.watersorter import *
from arduino.display import *
from arduino.bee import *
from arduino.sensors import *

hostname = ""
if hostname == "":
    print("IP adress :  ")
    hostname = input()
    if (len(hostname.split(".")) == 1):
        hostname = "192.168.1." + hostname
    print("Try reaching raspberry at IP " + hostname + "...")

# Connect to the Raspberry Pi and the different modules
MAX_VEL = 500
MAX_ROT = 6


m = Manager(hostname)
m.connect(10)



b = WheeledBase(m)


d = WaterSorter(m)
l = WaterLauncher(m)
a = BeeActuator(m)



    #	l = Module(m, 'display')
ssd = SevenSegments(m)
led1 = LEDMatrix(m, 1)
led2 = LEDMatrix(m, 2)


s_lat = Sensors(m, "sensorsLat")



s_front = Sensors(m, "sensorsAv")


s_back = Sensors(m, "sensorsAr")


