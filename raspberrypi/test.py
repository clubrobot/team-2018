from components import *
from watersorter import *
from waterlauncher import *

t = Manager()
t.connect()
w = WaterSorter(t)

l = WaterLauncher(t)
