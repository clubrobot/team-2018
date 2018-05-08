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

    ORANGE = 0
    BLACK = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4

    CUBES_ID = {ORANGE, BLACK, BLUE, GREEN, YELLOW}

    IMPOSSIBLE_CUBES = [[2], [], [3], [2], [], [3]]

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
        self.pattern = None


    def set_pattern(self, pattern):
        self.pattern = pattern

    def get_relative_position(self, closer_cube):
        if closer_cube == Cross.ORANGE:
            return [RobotArm.CLOSER_CUBE, RobotArm.LEFT_CUBE, RobotArm.RIGHT_CUBE, RobotArm.AWAY_CUBE, RobotArm.MIDDLE_CUBE]
        if closer_cube == Cross.BLACK:
            return [RobotArm.RIGHT_CUBE, RobotArm.CLOSER_CUBE, RobotArm.AWAY_CUBE, RobotArm.LEFT_CUBE, RobotArm.MIDDLE_CUBE]
        if closer_cube == Cross.GREEN:
            return [RobotArm.AWAY_CUBE, RobotArm.RIGHT_CUBE, RobotArm.LEFT_CUBE, RobotArm.CLOSER_CUBE, RobotArm.MIDDLE_CUBE]
        if closer_cube == Cross.BLUE:
            return [RobotArm.LEFT_CUBE, RobotArm.AWAY_CUBE, RobotArm.CLOSER_CUBE, RobotArm.RIGHT_CUBE, RobotArm.MIDDLE_CUBE]

    def get_opposite_cube(self, cube):
        if cube == Cross.ORANGE:
            return Cross.GREEN
        if cube == Cross.GREEN:
            return Cross.ORANGE
        if cube == Cross.BLUE:
            return Cross.BLACK
        if cube == Cross.BLACK:
            return Cross.BLUE

    def realize(self):
        time.sleep(5)
        opposite_cube = None
        for cube in Cross.CUBES_ID:
            if not cube in self.pattern and not cube in Cross.IMPOSSIBLE_CUBES[self.numberCross]:
                opposite_cube = cube

        if opposite_cube is not None:
            cube_to_reach = self.get_opposite_cube(opposite_cube)

        else:
            cube_to_reach = Cross.ORANGE

        theta = math.atan2(self.catchPoint[cube_to_reach][1] - self.preparationPoint[cube_to_reach][1],
                           self.catchPoint[cube_to_reach][0] - self.preparationPoint[cube_to_reach][0])
        self.logger("CUBES : ", "Go to cross", self.numberCross, "cube_to_reach n°", cube_to_reach)
        self.logger("CUBES", "Preparation Point : ", self.preparationPoint[cube_to_reach])
        self.logger("CUBES", "Catch Point : ", self.catchPoint[cube_to_reach])
        try:
            time.sleep(1)
            self.logger("CUBES : ", "Turn on the spot, theta : ", theta)
            self.mover.turnonthespot(theta, 3, Mover.AIM)
            time.sleep(1)
            self.logger("CUBES : ", "Go to catch position")
            try:
                self.wheeledbase.goto(*(self.catchPoint[cube_to_reach]))
            except RuntimeError:
                return
            self.wheeledbase.wait()
            time.sleep(1)
        except RuntimeError:
            pass

        cube_positions = self.get_relative_position(cube_to_reach)

        stack_height = 0
        if Cross.YELLOW not in self.pattern:
            for current_cube in self.pattern:
                self.arm.put_in_tank(cube_positions[current_cube], stack_height)
                stack_height += 1

            self.arm.put_in_tank(cube_positions[Cross.YELLOW], stack_height)

        else:
            remaining_cubes = Cross.CUBES_ID
            for pattern_cube in self.pattern:
                remaining_cubes.remove(pattern_cube)
            remaining_cubes.remove(opposite_cube)
            remaining_cube = remaining_cubes[0]

            if not (self.pattern.index(Cross.YELLOW) == 1):
                if self.pattern.index(Cross.YELLOW) == 0:
                    self.pattern.reverse()
                self.arm.put_in_tank(cube_positions[remaining_cube], stack_height)
                stack_height += 1

                for current_cube in self.pattern:
                    self.arm.put_in_tank(cube_positions[current_cube], stack_height)
                    stack_height += 1
            else:
                self.arm.put_in_temp(cube_positions[remaining_cube])
                for current_cube in self.pattern:
                    self.arm.put_in_tank(cube_positions[current_cube], stack_height)
                    stack_height += 1
                self.arm.put_from_temp_to_tank(stack_height)



       #cube_ = 0
       #for cube_pos in RobotArm.CUBES:
       #    self.logger("CUBES : ", "Catch cube n°", cube_)
       #    self.arm.set_pos(*cube_pos)
       #    time.sleep(2)
       #    self.arm.close_gripper()
       #    time.sleep(1)
       #    self.arm.set_z(RobotArm.MAX_Z-5)
       #    time.sleep(1)
       #    self.arm.set_z(RobotArm.MAX_Z)
       #    self.logger("CUBES : ", "Drop off the cube")
       #    self.arm.set_pos(*RobotArm.TANK)
       #    time.sleep(2)
       #    self.arm.set_z(cube_*5+RobotArm.MIN_Z)
       #    time.sleep(2)
       #    cube_ +=1
       #    self.arm.open_gripper()
       #    time.sleep(1)
       #    self.arm.set_pos(*RobotArm.TANK)
       #    time.sleep(2)

        self.arm.begin()
        time.sleep(2)



    def getAction(self):
        actions = [None]*1
        actions[0] = Action(self.preparationPoint[0],
                           lambda: self.realize(),
                           Cross.typ,
                           "Cross {} cube {}".format(self.numberCross, 0),
                           Cross.POINTS,
                           Cross.TIME)
        return actions


"""
class Dropper(Actionnable):
    typ = "Dropper"
    SPOT = 0
    def __init__(self, side, geo, arduinos, mover, logger, data):
        self.side = side
        self.geo = geo
        self.wheeledbase
"""