from components import *
from watersorter import *
from waterlauncher import *

t = Manager("192.168.1.21")
t.connect()
w = WaterSorter(t)

l = WaterLauncher(t)
