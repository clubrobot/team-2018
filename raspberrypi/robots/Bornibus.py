#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import math

from robots.cubes_manager           import CubeManagement
from robots.balls_manager           import Dispenser, Treatment, Shot
from robots.display_manager         import DisplayPoints
from robots.switch_manager_bornibus import Interrupteur_Bornibus, Abeille_Bornibus
from robots.mover                   import Mover, PositionUnreachable
from robots.heuristics              import Heuristics
from common.logger                  import Logger
from robots.beacons_manager         import BeaconsManagement
from beacons.balise_receiver        import BaliseReceiver
from robots.friend_manager import FriendManager
# Setup and launch the user interface
class Bornibus:
    cube ="cube"
    dispenser = "disp"
    shot = "shot"
    GREEN  = 0
    ORANGE = 1

    def __init__(self, side, roadmap, geogebra, wheeledbase, waterlauncher, watersorter, display, led1, led2, beeActioner,sensors_front, sensors_lat, sensors_back):
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
        self.logger   = Logger(Logger.SHOW)
        self.mover    = Mover(side, roadmap, self.arduinos, self.logger)
        self.data = dict()
        self.displayManager = DisplayPoints(display, led1, led2)
        self.cube_management = CubeManagement(self.roadmap, self.geogebra)



    def set_side(self,side):
        self.side = side
        self.action_list = [list(), list()]
        # Generate Dispenser
        self.d1 = Dispenser(1, self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger,
                            self.data)
        self.d2 = Dispenser(2, self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger,
                            self.data)
        self.d3 = Dispenser(3, self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger,
                            self.data)
        self.d4 = Dispenser(4, self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger,
                            self.data)
        # Generate buttons
        self.bee = Abeille_Bornibus(self.side, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger,
                           self.data)
        self.panel = Interrupteur_Bornibus(self.side, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger, self.data)

        # Generate balls manipulate
        self.treatment = Treatment(self.side, self.roadmap, self.geogebra, self.arduinos, self.displayManager,
                                   self.mover, self.logger, self.data)
        self.shot = Shot(self.side, self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover,
                         self.logger, self.data)

        # Generate predecessors list
        beeAct = self.bee.getAction()[0]
        panelAct = self.panel.getAction()[0]
        d1Act = self.d1.getAction()[0]
        d2Act = self.d2.getAction()[0]
        d3Act = self.d3.getAction()[0]
        d4Act = self.d4.getAction()[0]
        shortShot = self.shot.getAction()[0]
        #longShot0 = self.shot.getAction()[2]
        longShot1 = self.shot.getAction()[1]
        #longShot2 = self.shot.getAction()[4]
        treatmentAct = self.treatment.getAction()[0]

        if self.side == Bornibus.GREEN:
            dispMulti = d3Act
            dispMono = d1Act

        else:
            dispMulti = d2Act
            dispMono = d4Act

        self.action_list = [
           # beeAct,
           # dispMono,
           # shortShot,
           # dispMulti,
           # longShot1,
            treatmentAct,
            #panelAct,
        ]


        if self.side == Bornibus.GREEN:
            self.arduinos["wheeledbase"].set_position(650-112.5, 57.5, math.pi/2)
        else:
            self.arduinos["wheeledbase"].set_position(650-112.5, 3000-57.5, -math.pi/2)

    def run(self):
        self.displayManager.start()
        self.logger.reset_time()
        self.mover.reset()
        self.arduinos["watersorter"].set_shaker_velocity(400)
        self.arduinos["beeActioner"].close()
        self.arduinos["watersorter"].write_trash_unloader(40)
        self.arduinos["watersorter"].close_trash()

        self.data["nb_balls_in_unloader"] = 0

        for act in self.action_list:
            try:
                act.before_action()
                self.logger("MAIN : ", "Let's go to the next action : {}".format(act.typ))
                self.mover.goto(*act.actionPoint)
                self.logger("MAIN ; ", "Arrived on action point ! Go execute it =)")
                act()
                act.done.set()
            except PositionUnreachable:
                self.logger("MAIN : ", "Unreachable action")
                act.temp_disable(5)
            self.mover.reset()


if __name__ == '__main__':
    from robots.setup_bornibus import *

    print("DEBUT CHARGEMENT ROADMAP")
    geo = Geogebra('bornibus.ggb')
    rm = RoadMap.load(geo)
    print("Fin Chargement")

    br = BaliseReceiver("192.168.12.3")
    try:
        br.connect(timeout=1)
    except:
        print("BALISE : Not connected")
        pass

    bm = BeaconsManagement(br, "area.ggb")

    auto = Bornibus(0, rm, geo, wheeledbase, waterlauncher, watersorter, ssd, led1, led2, beeactuator, s_front, s_lat, s_back)
    auto.set_side(1)
    auto.run()
