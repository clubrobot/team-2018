#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math
import time

from robots.automateTools import AutomateTools
from robots.action import *
from robots.mover import Mover, PositionUnreachable


class Interrupteur(Actionnable):
    typ="Interrupteur"
    POINTS = 25
    TIME = 5
    def __init__(self,side, geo, arduinos, display, mover, logger):
        self.side=side
        self.mover = mover
        self.logger = logger
        self.wheeledbase = arduinos["wheeledbase"]
        self.display = display
        self.preparation=geo.get('Interrupteur'+str(self.side)+'_0')
        self.interrupteur=geo.get('Interrupteur'+str(self.side)+'_1')

    def realize(self,robot, display):
        theta = math.atan2(self.interrupteur[1]-self.preparation[1],self.interrupteur[0]-self.preparation[0])
        try:
            self.mover.turnonthespot(theta, try_limit=3, stategy=Mover.AIM)
            self.mover.gowall(try_limit=5, strategy=Mover.FAST, direction="forward")
        except PositionUnreachable:
            return
        display.addPoints(Interrupteur.POINTS)
        self.mover.withdraw(*self.preparation,direction="backward")

        #override Actionnable
    def getAction(self):
            return [Action( self.preparation,
                            lambda : self.realize(self.wheeledbase, self.display),
                            Interrupteur.typ,
                            "INTERRUPTEUR",
                            Interrupteur.POINTS,
                            Interrupteur.TIME)  ]

class Abeille(Actionnable):
    typ="Abeille"
    POINTS = 50
    TIME = 10
    def __init__(self, side, geo, arduinos, display, mover, logger):
        self.side=side
        self.logger = logger
        self.mover = mover
        self.wheeledbase =arduinos["wheeledbase"]
        self.display = display
        self.beeActioner = arduinos["beeActioner"]
        self.preparation=geo.get('Abeille'+str(self.side)+'_0')
        self.interrupteur=geo.get('Abeille'+str(self.side)+'_1')

    def realize(self,robot, display):
        try:
            self.mover.turnonthespot(math.pi,try_limit=3,stategy=Mover.AIM)
        except PositionUnreachable:
            return
        try:
            robot.purepursuit([self.preparation, self.interrupteur], direction="backward")
            robot.wait()
        except RuntimeError:
            return
        try:
            self.mover.turnonthespot(math.pi+(self.side*2-1)*math.pi/4, try_limit=3,stategy=Mover.AIM)
        except PositionUnreachable:
            return
        self.beeActioner.open()
        time.sleep(0.3)
        robot.set_velocities(0, -(self.side*2-1)*9)
        time.sleep(0.7)
        while not robot.isarrived():
            try:
                robot.goto(*self.preparation)
            except:
                robot.stop()
                robot.set_velocities(-100, 0)
                time.sleep(0.5)
        self.beeActioner.close()
        display.addPoints(Abeille.POINTS)

        #override Actionnable
    def getAction(self):
            return [Action( self.preparation,
                            lambda : self.realize(self.wheeledbase, self.display),
                            Interrupteur.typ,
                            "ABEILLE",
                            Abeille.POINTS,
                            Abeille.TIME)]

class Odometrie(Actionnable):
    typ="Odometrie"
    def __init__(self, side, geo,id):#id = 0 (vers le bas) ou 1(vers la droite)
        self.side=side
        self.preparation=geo.get('Odometrie'+str(self.side)+'_{'+str(id)+'}')
        self.mur=geo.get('Odometrie'+str(self.side)+'_{'+str(id)+',0}')

    def realize(self,robot):
        #print("Realisation")
        theta = math.atan2(self.mur[1]-self.preparation[1],self.mur[0]-self.preparation[0])
        AutomateTools.myTurnonthespot(robot,theta)
        path = [ self.preparation, self.mur]
        robot.purepursuit(path)
            #si on patine alors on stop l'action
        AutomateTools.myWait(robot,lambda : AutomateTools.stopThisAction)

        #override Actionnable
    def getAction(self,robot,builerCollector,waterDispenser):
            return [Action(self.preparation,
                    lambda : self.realize(robot),
                    Odometrie.typ, 
                    "ODOMETRIE") ]
