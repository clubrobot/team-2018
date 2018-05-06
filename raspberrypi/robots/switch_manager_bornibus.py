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
    def __init__(self,side, geo, arduinos, display, mover, logger, br, data):
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
        theta = math.atan2(self.interrupteur[1]-self.preparation[1],self.interrupteur[0]-self.preparation[0])
        try:
            self.logger("SWITCH : ", "Turn toward switch")
            self.mover.turnonthespot(theta, try_limit=3, stategy=Mover.AIM)
            self.logger("SWITCH : ", "Activate switch")
            self.mover.gowall(try_limit=5, strategy=Mover.SENSORS, direction="forward")
        except PositionUnreachable:
            return
        display.addPoints(Interrupteur.POINTS)
        self.logger("SWITCH : ", "Go back to preparation point")
        self.mover.withdraw(*self.preparation,direction="backward")
        self.actions[0].set_reliability(max(self.actions[0].reliability - 0.2, 0))
        self.watcher = Thread(target=self.watch, daemon=True)
        self.watcher.start()

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
        self.logger("BEE : ", "Turn toward bee")
        try:
            self.mover.turnonthespot(math.pi,try_limit=3,stategy=Mover.AIM)
        except PositionUnreachable:
            return

        self.logger("BEE : ", "Orientate to the bee")
        arrived = False
        nb_try = 0
        while not arrived and nb_try < 2:
            nb_try += 1
            try:
                robot.angpos_threshold.set(0.05)
                robot.purepursuit([self.preparation, self.interrupteur], direction="backward", lookahead=50,
                                  finalangle=math.pi/2+(self.side*2-1)*math.pi/4, lookaheadbis=400)
                robot.wait()
                arrived = True
            except RuntimeError:
                self.logger("BEE : ", "Can't orientate")
                robot.left_wheel_maxPWM.set(0.7)
                robot.right_wheel_maxPWM.set(0.7)
                robot.goto_delta(-150, 0)
                time.sleep(2)
                robot.left_wheel_maxPWM.set(1)
                robot.right_wheel_maxPWM.set(1)

        self.logger("BEE : ", "Activate arm")
        self.beeActioner.open()
        time.sleep(0.3)
        self.logger("BEE : ", "Activate bee")
        robot.set_velocities(0, -(self.side*2-1)*9)
        time.sleep(0.7)
        self.beeActioner.close()
        robot.stop()

        self.logger("Go back to action point")
        arrived = False
        while not arrived:
            try:
                self.mover.withdraw(*self.preparation, direction="forward")
                arrived = True
            except:
                robot.stop()
                robot.set_velocities(-100, 0)
                time.sleep(0.5)
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
