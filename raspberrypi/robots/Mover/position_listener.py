#!/usr/bin/env python3
# coding: utf-8


from threading        import Thread, Event
from sync_flag_signal import Signal
from time import sleep
from math import hypot

class PositionListener(Thread):
    def __init__(self, getter, timestep = 0.1, threadhold = 10):
        Thread.__init__(self)
        self.signal   = Signal()
        self.getter   = getter
        self.timestep = timestep
        self.stop  = Event()
        self.threadhold = threadhold
        self.error    = 0
        self.position = (-1000,-1000)# self.getter()
        #self.start()

    def run(self):
        while not self.stop.is_set():
            sleep(self.timestep)
            x , y = self.getter()

            if (hypot(y-self.position[1],x-self.position[0]) +self.error)>self.threadhold:
                self.signal.ping()
            
                self.error = 0
            else: 
                self.error +=hypot(y-self.position[1],x-self.position[0])
            self.position = (x,y)
           



if __name__ == '__main__':

    from sync_flag_signal import Flag

    class test():
        def __init__(self):
            self.position = (1000,1000)

        def set_position(self,x,y):
            self.position = (x,y)

        def get_position(self):
            return self.position

    def affiche():
        print("attention ca change")

    t = test()
    l = PositionListener(t.get_position)
    a = Flag(affiche)
    a.bind(l.signal)

