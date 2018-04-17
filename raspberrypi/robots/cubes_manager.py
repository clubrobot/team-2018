#!/usr/bin/env python3
#-*- coding: utf-8 -*-

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
