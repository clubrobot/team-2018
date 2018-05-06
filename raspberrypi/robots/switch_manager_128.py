#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math
import time
from threading import Thread

from robots.automateTools import AutomateTools
from robots.action import *
from robots.mover import Mover, PositionUnreachable
from robots.switch_manager import Interrupteur, Abeille


class Interrupteur_128(Interrupteur):
    def __init__(self,side, geo, arduinos, display, mover, logger, br, data):
        super(Interrupteur_128, self).__init__(side, geo, arduinos, display, mover, logger, br, data)

    def realize(self,robot, display):
        theta = math.atan2(self.interrupteur[1]-self.preparation[1],self.interrupteur[0]-self.preparation[0]) + math.pi
        try:
            self.logger("SWITCH : ", "Turn toward switch")
            self.mover.turnonthespot(theta, try_limit=3, stategy=Mover.AIM)
            self.logger("SWITCH : ", "Activate switch")
            self.mover.gowall(try_limit=5, strategy=Mover.POSITION, direction="backward", position=self.interrupteur)
        except PositionUnreachable:
            return
        display.addPoints(Interrupteur.POINTS)
        self.logger("SWITCH : ", "Go back to preparation point")
        self.mover.withdraw(*self.preparation,direction="forward")
        self.actions[0].set_reliability(max(self.actions[0].reliability - 0.2, 0))
        self.watcher = Thread(target=self.watch, daemon=True)
        self.watcher.start()


class Abeille_128(Abeille):
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
        while not arrived and nb_try < 2:
            nb_try += 1
            try:
                robot.purepursuit([self.preparation, self.interrupteur], direction="forward", lookahead=50,
                                  finalangle=(self.side*2-1)*math.pi/4, lookaheadbis=400)
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
        time.sleep(0.4)
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
