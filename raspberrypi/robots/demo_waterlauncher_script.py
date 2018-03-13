from demo import *
import time
t=Demo()
t.connect()
t.close_trash()
t.set_motor_velocity(143)
while True:
    t.open_indoor()
    time.sleep(0.5)
    t.close_indoor()
    time.sleep(0.5)
    t.open_outdoor()
    #time.sleep(0.5)
    time.sleep(1)
    t.close_outdoor()
    #t.open_indoor()
    time.sleep(0.5)
    #t.close_indoor()
    #time.sleep(0.5)
    #time.sleep(1)
    #t.open_trash()
    #time.sleep(2)
    #t.close_trash()




