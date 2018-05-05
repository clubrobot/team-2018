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
    if (len(hostname) == 0):
        hostname = "127.0.0.1"
    elif (len(hostname.split(".")) == 1):
        hostname = "192.168.1." + hostname
    print("Try reaching raspberry at IP " + hostname + "...")

# Connect to the Raspberry Pi and the different modules
MAX_VEL = 500
MAX_ROT = 6


manager = Manager(hostname)
manager.connect(10)



wheeledbase = WheeledBase(manager)


watersorter = WaterSorter(manager)
watersorter.open_indoor()
watersorter.close_outdoor()
waterlauncher = WaterLauncher(manager)
beeactuator = BeeActuator(manager)



    #	l = Module(m, 'display')
ssd = SevenSegments(manager)
led1 = LEDMatrix(manager, 1)
led2 = LEDMatrix(manager, 2)


s_lat = Sensors(manager, "sensorsLat")



s_front = Sensors(manager, "sensorsAv")


s_back = Sensors(manager, "sensorsAr")


