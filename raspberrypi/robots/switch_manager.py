#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math
import time
from threading import Thread

from robots.automateTools import AutomateTools
from robots.action import *
from robots.mover import Mover, PositionUnreachable


class Interrupteur(Actionnable):
    typ="Interrupteur"
    POINTS = 25
    TIME = 5
    def __init__(self,side, geo, arduinos, display, mover, logger, data):
        self.side=side
        self.mover = mover
        self.logger = logger
        self.wheeledbase = arduinos["wheeledbase"]
        self.display = display
        self.preparation=geo.get('Interrupteur'+str(self.side)+'_0')
        self.interrupteur=geo.get('Interrupteur'+str(self.side)+'_1')
        self.data = data
        self.beacon_receiver = br
        self.actions = []
        self.watcher = None

    def realize(self,robot, display):
        raise NotImplementedError("Need implementation")
        return

        #override Actionnable
    def getAction(self):
        self.actions =  [Action( self.preparation,
                        lambda : self.realize(self.wheeledbase, self.display),
                            Interrupteur.typ,
                            "INTERRUPTEUR",
                            Interrupteur.POINTS,
                            Interrupteur.TIME)  ]
        return self.actions

    def watch(self):
        self.logger("SWITCH WATCHER : ", "Start thread")
        time.sleep(7)
        if not self.beacon_receiver.get_panel_status():
            self.logger("SWITCH WATCHER : ", "Panel off")
            self.actions[0].done.clear()
            self.display.removePoints(Interrupteur.POINTS)

        else:
            self.logger("SWITCH WATCHER : ", "Panel on")



class Abeille(Actionnable):
    typ="Abeille"
    POINTS = 50
    TIME = 10
    def __init__(self, side, geo, arduinos, display, mover, logger, data):
        self.side=side
        self.logger = logger
        self.mover = mover
        self.wheeledbase =arduinos["wheeledbase"]
        self.display = display
        self.beeActioner = arduinos["beeActioner"]
        self.preparation=geo.get('Abeille'+str(self.side)+'_0')
        self.interrupteur=geo.get('Abeille'+str(self.side)+'_1')
        self.data = data

    def realize(self,robot, display):
        return

        #override Actionnable
    def getAction(self):
            return [Action( self.preparation,
                            lambda : self.realize(self.wheeledbase, self.display),
                            Interrupteur.typ,
                            "ABEILLE",
                            Abeille.POINTS,
                            Abeille.TIME)]
