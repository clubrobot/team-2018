#!/usr/bin/env python3
#-*- coding: utf-8 -*-


from robots.action import Actionnable, Action
from robots.mover import Mover
from math import pi

class Photograph(Actionnable):
    typ = "Photograph"
    def __init__(self, side, geo, patern, arduinos, mover, logger, data):
        self.side = side
        self.geo  = geo
        self.patern = patern
        self.wheeledbase = arduinos["wheeledbase"]
        self.camera      = arduinos["camera"]
        self.mover = mover
        self.logger = logger
        self.data   = data
        self.preparation = self.geo.get('Photography')


    def realize(self):
        self.mover.turnonthespot(-pi/2,3,Mover.AIM)
        self.patern.take_photo()


    def getAction(self):
            return [Action(self.preparation,
                    lambda : self.realize(),
                     Photograph.typ,
                    "Photography",
                    0,
                    0) ]


