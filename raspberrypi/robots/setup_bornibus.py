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

try:
    m = Manager(hostname)
    m.connect(10)
except:
    raise
    m = Manager()
    m.connect(10)

try:
    b = WheeledBase(m)
except:
    print('\'wheeledbase\' not connected')

try:
    d = WaterSorter(m)
    l = WaterLauncher(m)
    a = BeeActuator(m)
except:
    print('\'wattershooter\' not connected')

try:
    #	l = Module(m, 'display')
    ssd = SevenSegments(m)
    led1 = LEDMatrix(m, 1)
    led2 = LEDMatrix(m, 2)
except:
    print('\'display\' not connected')
try:
    s_lat = Sensors(m, "sensorsLat")
except:
    print('\'sensors lat\' not connected')

try:
    s_front = Sensors(m, "sensorsAv")
except:
    print('\'sensors front\' not connected')

try:
    s_back = Sensors(m, "sensorsAr")
except:
    print('\'sensors back\' not connected')

#geo = Geogebra('bornibus.ggb')
#rm = RoadMap.load(geo)