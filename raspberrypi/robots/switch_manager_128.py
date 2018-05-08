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
            self.mover.turnonthespot(theta+math.pi, try_limit=3, stategy=Mover.AIM)
            self.logger("SWITCH : ", "Activate switch")
            self.mover.gowall(try_limit=5, strategy=Mover.POSITION, direction="forward", position=self.interrupteur)
        except PositionUnreachable:
            return
        display.addPoints(Interrupteur.POINTS)
        self.logger("SWITCH : ", "Go back to preparation point")
        self.mover.withdraw(*self.preparation,direction="backward")
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




class Odometry(Actionnable):
    typ="Odometrie"
    def __init__(self, side, geo, arduinos, mover, logger, data):

        self.side=side
        self.mover = mover
        self.logger = logger
        self.data = data
        self.wheeledbase = arduinos["wheeledbase"]
        self.preparation = geo.get('Odometry'+str(self.side))
        self.wall  = [geo.get('Odometry'+str(self.side)+'_0'),geo.get('Odometry' + str(self.side) + '_1')]

    def realize(self):
        self.logger("ODOMETRY : ", "Launch a mover turnOnTheSpot")
        try:
            self.mover.turnonthespot([-math.pi/2,math.pi][0], 3, Mover.AIM)
        except PositionUnreachable:
            self.logger("ODOMETRY :", "Angle not reachable, odometry aborded")
            self.wheeledbase.left_wheel_maxPWM.set(1)
            self.wheeledbase.right_wheel_maxPWM.set(1)
            return
        try:
            self.wheeledbase.set_velocities(200, 0)
            self.wheeledbase.left_wheel_maxPWM.set(0.8)
            self.wheeledbase.right_wheel_maxPWM.set(0.8)
            self.wheeledbase.wait()
        except RuntimeError:

            # Do an odometry recalibration
            xref, yref = self.wall[0]
            thetaref = [-math.pi/2,math.pi][0]
            #		thetaref = wheeledbase.get_position()[2]
            xthought, ythought = self.wheeledbase.get_position()[:2]
            offset = math.hypot(xref - xthought, yref - ythought) * math.cos(
                thetaref - math.atan2(yref - ythought, xref - xthought))
            xthought += offset * math.cos(thetaref)
            ythought += offset * math.sin(thetaref)
            self.wheeledbase.set_position(xthought, ythought, thetaref)

        self.mover.withdraw(self.preparation[0], self.preparation[1],"backward",Mover.SOFT)

        try:
            self.mover.turnonthespot([-math.pi/2,math.pi][1], 3, Mover.AIM)
        except PositionUnreachable:
            self.logger("ODOMETRY :", "Angle not reachable, odometry aborded")
            self.wheeledbase.left_wheel_maxPWM.set(1)
            self.wheeledbase.right_wheel_maxPWM.set(1)
            return
        try:
            self.wheeledbase.set_velocities(200, 0)
            self.wheeledbase.left_wheel_maxPWM.set(0.8)
            self.wheeledbase.right_wheel_maxPWM.set(0.8)
            self.wheeledbase.wait()
        except RuntimeError:

            # Do an odometry recalibration
            xref, yref = self.wall[1]
            thetaref = [-math.pi/2,math.pi][1]
            #		thetaref = wheeledbase.get_position()[2]
            xthought, ythought = self.wheeledbase.get_position()[:2]
            offset = math.hypot(xref - xthought, yref - ythought) * math.cos(
                thetaref - math.atan2(yref - ythought, xref - xthought))
            xthought += offset * math.cos(thetaref)
            ythought += offset * math.sin(thetaref)
            self.wheeledbase.set_position(xthought, ythought, thetaref)

        self.mover.withdraw(self.preparation[0], self.preparation[1],"backward",Mover.SOFT)


    def getAction(self):
            return [Action(self.preparation,
                    lambda : self.realize(),
                     Odometry.typ,
                    "Odometry",
                    0,
                    0) ]

