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
    def __init__(self,side, geo, arduinos, display, mover, logger, data):
        Interrupteur.__init__(self, side, geo, arduinos, display, mover, logger, data)

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
            self.mover.turnonthespot(math.pi, try_limit=3, stategy=Mover.AIM)
        except PositionUnreachable:
            return

        self.logger("BEE : ", "Orientate to the bee")
        is_arrived = False
        robot.set_velocities(-200,0)
        try:
            while True:
                robot.isarrived()
                time.sleep(0.1)
        except RuntimeError:
            robot.goto_delta(70, 0)
            try:
                robot.wait()
            except RuntimeError:
                pass

            try:
                robot.angpos_threshold.set(0.05)
                self.mover.turnonthespot(math.pi+math.pi / 2 + (self.side * 2 - 1) * math.pi / 4, 2,Mover.AIM)
            except PositionUnreachable:
                return

        self.logger("BEE : ", "Activate arm")
        self.beeActioner.open()
        time.sleep(0.3)
        self.logger("BEE : ", "Activate bee")
        robot.set_velocities(0, -(self.side * 2 - 1) * 9)
        time.sleep(1.1)
        self.beeActioner.close()
        robot.stop()
        time.sleep(0.2)
        try:
            self.mover.turnonthespot(math.pi + math.pi / 2 + (self.side * 2 - 1) * math.pi / 4, 2, Mover.AIM)
        except RuntimeError:
            return
        self.logger("BEE : ", "Activate arm")
        self.beeActioner.open()
        time.sleep(0.3)
        self.logger("BEE : ", "Activate bee")
        robot.set_velocities(0, -(self.side * 2 - 1) * 9)
        time.sleep(1.1)
        self.beeActioner.close()
        robot.stop()
        time.sleep(0.2)
        self.logger("Go back to action point")
        arrived = False
        try:
            self.mover.turnonthespot(0,try_limit=3,stategy=Mover.AIM)
        except PositionUnreachable:
            pass
        while not arrived:
            try:
                robot.goto(*self.preparation)
                arrived = True
            except:
                robot.stop()
                robot.set_velocities(100, 0)
                time.sleep(0.5)
        display.addPoints(Abeille.POINTS)


