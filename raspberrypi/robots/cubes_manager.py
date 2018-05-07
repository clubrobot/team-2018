#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math
import time

from robots.automateTools import AutomateTools
from robots.action import Action, Actionnable
from robots.mover import Mover, PositionUnreachable
from arduino.arm import RobotArm

class CubeManagement():
    def __init__(self, rm, geo):
        self.roadmap  = rm
        self.geogebra = geo
        self.obstacles = list()
        for i in range(6):
            points = self.geogebra.getall("CroixObstacle{}_*".format(i))
            self.obstacles.append(self.roadmap.create_obstacle(points))
            self.obstacles[i].set_position(0,0,0)

    def disable(self, id):    
        self.obstacles[id].set_position(2000,3000,0)

    def enable(self, id):
        self.obstacles[id].set_position(0,0,0)


class Cross(Actionnable):
    typ = "catch_cube"
    POINTS = 1
    TIME = 1

    def __init__(self, side, numberCross, rm, geo, arduinos, mover, logger, data):
        self.side = side
        self.rm = rm
        self.mover = mover
        self.geo = geo
        self.logger = logger
        self.numberCross = numberCross
        self.wheeledbase = arduinos["wheeledbase"]
        self.arm = arduinos["robot_arm"]
        self.catchPoint = [None]*4
        self.preparationPoint = [None]*4
        for cube in range(4):
            self.catchPoint[cube] = self.geo.get("Croix"+ str(self.numberCross) + "_{"+ str(cube) + "1}")
            self.preparationPoint[cube] = self.geo.get("Croix"+ str(self.numberCross) + "_{"+ str(cube) + "0}")

        self.data = data

    def realize(self, cube):
        time.sleep(5)
        theta = math.atan2(self.catchPoint[cube][1] - self.preparationPoint[cube][1],
                           self.catchPoint[cube][0] - self.preparationPoint[cube][0])
        self.logger("CUBES : ", "Go to cross", self.numberCross, "cube n°", cube)
        self.logger("CUBES", "Preparation Point : ", self.preparationPoint[cube])
        self.logger("CUBES", "Catch Point : ", self.catchPoint[cube])
        try:
            time.sleep(1)
            self.logger("CUBES : ", "Turn on the spot, theta : ", theta)
            self.mover.turnonthespot(theta, 3, Mover.AIM)
            time.sleep(1)
            current_position = self.wheeledbase.get_position()
            self.logger("CUBES : ", "Go to catch position")
            try:
                self.wheeledbase.goto(*self.catchPoint[cube])
            except RuntimeError:
                return
            self.wheeledbase.wait()
            time.sleep(1)
        except RuntimeError:
            pass
        cube_ = 0
        for cube_pos in RobotArm.CUBES:
            self.logger("CUBES : ", "Catch cube n°", cube_)
            self.arm.set_pos(*cube_pos)
            time.sleep(2)
            self.arm.close_gripper()
            time.sleep(1)
            self.arm.set_z(RobotArm.MAX_Z-5)
            time.sleep(1)
            self.arm.set_z(RobotArm.MAX_Z)
            self.logger("CUBES : ", "Drop off the cube")
            self.arm.set_pos(*RobotArm.TANK)
            time.sleep(2)
            self.arm.set_z(cube_*5+RobotArm.MIN_Z)
            time.sleep(2)
            cube_ +=1
            self.arm.open_gripper()
            time.sleep(1)
            self.arm.set_pos(*RobotArm.TANK)
            time.sleep(2)

        self.arm.begin()
        time.sleep(2)



    def getAction(self):
        actions = [None]*4
        actions[0] = Action(self.preparationPoint[0],
                           lambda: self.realize(0),
                           Cross.typ,
                           "Cross {} cube {}".format(self.numberCross, 0),
                           Cross.POINTS,
                           Cross.TIME)
        actions[1] = Action(self.preparationPoint[1],
                           lambda: self.realize(1),
                           Cross.typ,
                           "Cross {} cube {}".format(self.numberCross, 1),
                           Cross.POINTS,
                           Cross.TIME)
        actions[2] = Action(self.preparationPoint[2],
                           lambda: self.realize(2),
                           Cross.typ,
                           "Cross {} cube {}".format(self.numberCross, 2),
                           Cross.POINTS,
                           Cross.TIME)
        actions[3] = Action(self.preparationPoint[3],
                           lambda: self.realize(3),
                           Cross.typ,
                           "Cross {} cube {}".format(self.numberCross, 3),
                           Cross.POINTS,
                           Cross.TIME)
        return actions

