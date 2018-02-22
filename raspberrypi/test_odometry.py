from components import *
from wheeledbase import *
import serialtalks
import time
import sys
t  = Manager()
try:
    t.connect()
except tcptalks.ForeverAloneError:
    print("Plz start the server with : robot server&")
    
try:
    b = WheeledBase(t)
except serialtalks.ConnectionFailedError:
    print("Plz press the restart button ! or replug ESP32")
    input()
    sys.exit(0)




while True:
    print(b.get_codewheels_counter())
    time.sleep(0.002)
