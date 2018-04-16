#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time


from robots.cubes_manager        import CubeManagement
from robots.balls_manager        import Dispenser, Treatment, Shot
from robots.display_manager      import DisplayPoints
from robots.switch_manager       import Interrupteur, Abeille
from robots.mover                import Mover



# Setup and launch the user interface
class Bornibus:

    cube="cube"
    dispenser = "disp"
    shot = "shot"
    GREEN  = 0
    ORANGE = 1
    def __init__(self, side, roadmap, geogebra, wheeledbase, waterlauncher, watersorter, display, beeActioner,sensors_front, sensors_lat, sensors_back):
        # Save arduinos
        self.wheeledbase   = wheeledbase
        self.waterlauncher = waterlauncher
        self.watersorter   = watersorter
        self.display       = display
        self.beeActioner   = beeActioner

        # Save annexes inf
        self.side     = side
        self.roadmap  = roadmap
        self.geogebra = geogebra
        self.mover    = Mover(side, roadmap, wheeledbase, sensors_front, sensors_lat, sensors_back)

        # Apply cube obstacle
        self.cube_management = CubeManagement(self.roadmap, self.geogebra)

        self.action_list = [list(),list()]
        
        self.displayManager = DisplayPoints(self.display)

        # Generate Dispenser
        self.d1 = Dispenser(1,self.roadmap, self.geogebra, self.wheeledbase, self.watersorter, self.displayManager, self.mover)
        self.d2 = Dispenser(2,self.roadmap, self.geogebra, self.wheeledbase, self.watersorter, self.displayManager, self.mover)
        self.d3 = Dispenser(3,self.roadmap, self.geogebra, self.wheeledbase, self.watersorter, self.displayManager, self.mover)
        self.d4 = Dispenser(4,self.roadmap, self.geogebra, self.wheeledbase, self.watersorter, self.displayManager, self.mover)
        # Generate buttons
        self.bee   = Abeille(self.side, self.geogebra, self.wheeledbase, self.displayManager, self.beeActioner, self.mover)
        self.panel = Interrupteur(self.side, self.geogebra, self.wheeledbase, self.displayManager, self.mover)

        # Generate balls manipulate
        self.treatment = Treatment(self.side, self.roadmap, self.geogebra, self.wheeledbase, self.watersorter, self.mover)
        self.shot      = Shot     (self.side, self.roadmap, self.geogebra, self.wheeledbase, self.watersorter, self.waterlauncher, self.displayManager,self.mover)


        # Generate order list
        self.action_list[Bornibus.GREEN] = [
            self.bee.getAction()[0],
            self.panel.getAction()[0],
            self.d1.getAction()[0],
            self.shot.getAction()[0],
            self.d3.getAction()[0],
            self.shot.getAction()[2],
            self.treatment.getAction()[0],
            ]
        
        self.action_list[Bornibus.ORANGE] = [
            self.bee.getAction()[0],
            self.panel.getAction()[0],
            self.d4.getAction()[0],
            self.shot.getAction()[0],
            self.d2.getAction()[0],
            self.shot.getAction()[2],
            self.treatment.getAction()[0],
            ]
            
    def run(self):
        if self.side == Bornibus.GREEN:
            self.wheeledbase.set_position(592, 290,0)
        else:
            self.wheeledbase.set_position(592,2710,0)
        self.wheeledbase.lookahead.set(200)
        self.wheeledbase.max_linvel.set(500)
        self.wheeledbase.max_angvel.set(6)
        self.beeActioner.close()
        self.watersorter.close_trash_unloader()
        while len(self.action_list[self.side])!=0:
            act = self.action_list[self.side].pop(0)
            currentPosXY=self.wheeledbase.get_position()[:2]
            path = self.roadmap.get_shortest_path( currentPosXY ,act.actionPoint )
            print(path)
            self.mover.goto(*act.actionPoint)
            print("Make action {}".format(act.typ))
            act()
            self.wheeledbase.max_linvel.set(500)
            self.wheeledbase.max_angvel.set(6)





