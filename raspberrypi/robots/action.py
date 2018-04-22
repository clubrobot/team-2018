#!/usr/bin/env python3
# coding: utf-8

class Action():
    def __init__(self,actionPoint,actionFunction,typ, name, points, time):
        self.actionPoint=actionPoint
        self.actionFunction=actionFunction
        self.typ=typ
        self.predecessors = []
        self.done = False
        self.name = name
        self.points = points
        self.combinations = []
        self.reliability = 1
        self.time = time
        
    def __call__(self):
        self.actionFunction()

    def realize(self):
        self()

    def set_predecessors(self, predecessors):
        self.predecessors = predecessors

    def check_impossible_combinations(self, actions):
        for combi in self.combinations:
            if combi():
                return False
        return True

    def set_impossible_combination(self, lambd):
        self.combinations += [lambd]

    def set_reliability(self, rel):
        self.reliability = rel

    def __bool__(self):
        return self.done

class Actionnable():
    def getAction(self):
        raise NotImplementedError("Need implementation")
