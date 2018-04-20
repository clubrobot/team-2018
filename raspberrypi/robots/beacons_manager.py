#!/usr/bin/env python3
# coding: utf-8

from time import sleep
from threading import Thread, Event
from beacons.anchor import Anchor
from common.geogebra import Geogebra

REDUCE_CONSTANT = 0.05
INCREASE_CONSTANT = 0.10
class Area:
    def __init__(self, points_list):
        self.points = points_list
        self.value = 0
    def reduce(self):
        self.value = max(self.value-REDUCE_CONSTANT,0)

    def increase(self, x, y):
        for i in range(len(self.points)):
            ((x_1, y_1), (x_2, y_2)) = (self.points[i], self.points[(i+1)%len(self.points)])
            vect = (x_2-x_1)*(y-y_1) - (y_2-y_1)*(x-x_1)
            if vect<0:
                return
        self.value = min(self.value+INCREASE_CONSTANT,1)


class BeaconsManagement(Thread):
    def __init__(self, anchor, file, timestep=0.1):
        Thread.__init__(self)
        self.daemon = True
        self.timestep = timestep
        self.anchor = anchor
        self.geogebra = Geogebra(file)
        self.areas = dict()
        self.running = Event()


    def create_area(self, name,  patern=None):
        points =  self.geogebra.getall(patern)
        if len(points)<3:
            raise RuntimeError("No enough points to create an area !")
        self.areas[name] = Area(points)
        return name

    def get_area_value(self, name):
        try:
            return  self.areas[name].value
        except KeyError:
            raise RuntimeError("No area called {}.".format(name))

    def run(self):
        self.running.set()
        while self.running.is_set():
            sleep(self.timestep)
            # Decrease the value of all area
            for area in self.areas.values() : area.reduce()
            # Increase the area of all area with a robot on.
            for robot in range(2):
                for area in self.areas.values(): area.increase(*self.anchor.get_position(robot))
