#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time


from robots.cubes_manager        import CubeManagement
from robots.balls_manager        import Dispenser, Treatment, Shot
from robots.display_manager      import DisplayPoints
from robots.switch_manager       import Interrupteur, Abeille
from robots.mover                import Mover
from robots.heuristics           import Heuristics


# Setup and launch the user interface
class Bornibus:

    cube ="cube"
    dispenser = "disp"
    shot = "shot"
    GREEN  = 0
    ORANGE = 1

    def __init__(self, side, roadmap, geogebra, wheeledbase, waterlauncher, watersorter, display, beeActioner,sensors_front, sensors_lat, sensors_back):
        # Save arduinos
        self.arduinos = dict(wheeledbase=wheeledbase,
                             waterlauncher=waterlauncher,
                             watersorter=watersorter,
                             display=display,
                             beeActioner=beeActioner,
                             sensors_front=sensors_front,
                             sensors_lat=sensors_lat,
                             sensors_back=sensors_back
                             )


        # Save annexes inf
        self.side     = side
        self.roadmap  = roadmap
        self.geogebra = geogebra
        self.mover    = Mover(side, roadmap, self.arduinos)

        # Apply cube obstacle
        self.cube_management = CubeManagement(self.roadmap, self.geogebra)

        self.action_list = [list(),list()]

        self.displayManager = DisplayPoints(display)

        # Generate Dispenser
        self.d1 = Dispenser(1,self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover)
        self.d2 = Dispenser(2,self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover)
        self.d3 = Dispenser(3,self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover)
        self.d4 = Dispenser(4,self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover)
        # Generate buttons
        self.bee   = Abeille(self.side, self.geogebra,  self.arduinos, self.displayManager, self.mover)
        self.panel = Interrupteur(self.side, self.geogebra, self.arduinos, self.displayManager, self.mover)

        # Generate balls manipulate
        self.treatment = Treatment(self.side, self.roadmap, self.geogebra, self.arduinos, self.mover)
        self.shot      = Shot     (self.side, self.roadmap, self.geogebra, self.arduinos, self.displayManager,self.mover)

        self.heuristics = Heuristics(self.action_list[self.side])

        #Generate predecessors list
        beeAct = self.bee.getAction()[0]
        panelAct = self.panel.getAction()[0]
        d1Act = self.d1.getAction()[0]
        d2Act = self.d2.getAction()[0]
        d3Act = self.d3.getAction()[0]
        d4Act = self.d4.getAction()[0]
        shortShot = self.shot.getAction()[0]
        longShot = self.shot.getAction()[2]
        treatmentAct = self.treatment.getAction()[0]

        if self.side == Bornibus.GREEN:
            shortShot.set_predecessors([d1Act])
            longShot.set_predecessors([d3Act])

        if self.side == Bornibus.ORANGE:
            shortShot.set_predecessors([d4Act])
            longShot.set_predecessors([d2Act])

        treatmentAct.set_predecessors([longShot])

        # Generate order list
        self.action_list[Bornibus.GREEN] = [
            beeAct,
            panelAct,
            d1Act,
            shortShot,
            d3Act,
            longShot,
            treatmentAct,
        ]

        self.action_list[Bornibus.ORANGE] = [
            beeAct,
            panelAct,
            d4Act,
            shortShot,
            d2Act,
            longShot,
            treatmentAct,
        ]

    def run(self):
        self.arduinos["wheeledbase"].lookahead.set(200)
        self.arduinos["wheeledbase"].max_linvel.set(500)
        self.arduinos["wheeledbase"].max_angvel.set(6)
        self.arduinos["beeActioner"].close()
        self.arduinos["watersorter"].close_trash_unloader()
        act = self.heuristics.getBest()
        while act is not None:
            print("Make action {}".format(act.name))
            # act()
            act.done = True
            act = h.getBest()
            self.arduinos["wheeledbase"].max_linvel.set(500)
            self.arduinos["wheeledbase"].max_angvel.set(6)





