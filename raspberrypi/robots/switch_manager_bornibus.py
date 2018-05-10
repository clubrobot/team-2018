#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math
import time
from threading import Thread

from robots.automateTools import AutomateTools
from robots.action import *
from robots.mover import Mover, PositionUnreachable
from robots.switch_manager import Abeille, Interrupteur


class Interrupteur_Bornibus(Interrupteur):
    def __init__(self,side, geo, arduinos, display, mover, logger, br, data):
        Interrupteur.__init__(self, side, geo, arduinos, display, mover, logger, br, data)

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




class Abeille_Bornibus(Abeille):
    def __init__(self, side, geo, arduinos, display, mover, logger, data):
        Abeille.__init__(self, side, geo, arduinos, display, mover, logger, data)

    def realize(self,robot, display):
        self.logger("BEE : ", "Turn toward bee")
        try:
            self.mover.turnonthespot(0,try_limit=3,stategy=Mover.AIM)
        except PositionUnreachable:
            return

        self.logger("BEE : ", "Orientate to the bee")
        arrived = False
        nb_try = 0
        time.sleep(0.05)
        while not arrived and nb_try < 2:
            nb_try += 1
            try:
                self.wheeledbase.goto(*self.interrupteur,direction="forward")
                arrived = True
            except RuntimeError:
                self.wheeledbase.goto_delta(-150,0)
                try:
                    self.wheeledbase.wait()
                except RuntimeError:
                    pass

        if arrived:
            try:
                self.mover.turnonthespot(-math.pi/2,2,Mover.AIM)
            except PositionUnreachable:
                return
        else:
            return
        if self.side==0:
            self.wheeledbase.goto_delta(200,0)
            try:
                self.wheeledbase.wait()
            except RuntimeError:
                pass
        self.logger("BEE : ", "Activate arm")
        self.beeActioner.open()
        time.sleep(0.3)
        self.logger("BEE : ", "Activa te bee")
        self.wheeledbase.goto_delta((self.side*2-1)*300,0)
        try:
            self.wheeledbase.wait()
        except RuntimeError:
            pass

        self.beeActioner.close()
        self.wheeledbase.stop()

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


