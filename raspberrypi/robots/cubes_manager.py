#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math
import time

from robots.automateTools import AutomateTools
from robots.action import Action, Actionnable
from robots.mover import Mover, PositionUnreachable

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
        self.catchPoint = []
        self.preparationPoint = []
        for cube in range(4):
            self.catchPoint += [self.geo.get("Croix"+ str(self.numberCross) + "_{"+ str(cube) + "1}")]
            self.preparationPoint += [self.geo.get("Croix"+ str(self.numberCross) + "_{"+ str(cube) + "0}")]

        self.data = data
    def realize(self, cube):
        theta = math.atan2(self.preparationPoint[cube][1] - self.catchPoint[cube][1],
                           self.preparationPoint[cube][0] - self.catchPoint[cube][0]) + math.pi/2
        try:
            time.sleep(1)
            self.mover.turnonthespot(theta, 3, Mover.AIM)
            time.sleep(1)
            current_position = self.wheeledbase.get_position()
            self.wheeledbase.goto_delta(self.catchPoint[cube][0] - current_position[0],
                                  self.catchPoint[cube][1] - current_position[1])
        except RuntimeError:
            pass

    def getAction(self):
        actions = []
        for cube in range(4):
            actions += [Action(self.preparationPoint[cube],
                               lambda: self.realize(cube),
                               Cross.typ,
                               "Cross {} cube {}".format(self.numberCross, cube),
                               Cross.POINTS,
                               Cross.TIME)]
        return actions

