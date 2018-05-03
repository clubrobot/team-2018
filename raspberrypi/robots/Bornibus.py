#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time


from robots.cubes_manager        import CubeManagement
from robots.balls_manager        import Dispenser, Treatment, Shot
from robots.display_manager      import DisplayPoints
from robots.switch_manager       import Interrupteur, Abeille
from robots.mover                import Mover
from robots.heuristics           import Heuristics
from common.logger               import Logger
from robots.beacons_manager      import BeaconsManagement
from beacons.balise_receiver     import BaliseReceiver

# Setup and launch the user interface
class Bornibus:

    cube ="cube"
    dispenser = "disp"
    shot = "shot"
    GREEN  = 0
    ORANGE = 1

    def __init__(self, side, roadmap, geogebra, wheeledbase, waterlauncher, watersorter, display, led1, led2, beeActioner,sensors_front, sensors_lat, sensors_back, br, bm):
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
        self.mover    = Mover(side, roadmap, self.arduinos, self.logger, br)
        self.data = dict()

        # Apply cube obstacle
        self.cube_management = CubeManagement(self.roadmap, self.geogebra)

        self.action_list = [list(),list()]

        self.displayManager = DisplayPoints(display, led1, led2)

        # Generate Dispenser
        self.d1 = Dispenser(1,self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger, self.data)
        self.d2 = Dispenser(2,self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger, self.data)
        self.d3 = Dispenser(3,self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger, self.data)
        self.d4 = Dispenser(4,self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger, self.data)
        # Generate buttons
        self.bee   = Abeille(self.side, self.geogebra,  self.arduinos, self.displayManager, self.mover, self.logger, self.data)
        self.panel = Interrupteur(self.side, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger, self.data)

        # Generate balls manipulate
        self.treatment = Treatment(self.side, self.roadmap, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger, self.data)
        self.shot      = Shot     (self.side, self.roadmap, self.geogebra, self.arduinos, self.displayManager,self.mover, self.logger, self.data)

        #Generate predecessors list
        beeAct = self.bee.getAction()[0]
        panelAct = self.panel.getAction()[0]
        d1Act = self.d1.getAction()[0]
        d2Act = self.d2.getAction()[0]
        d3Act = self.d3.getAction()[0]
        d4Act = self.d4.getAction()[0]
        shortShot = self.shot.getAction()[0]
        longShot0 = self.shot.getAction()[2]
        longShot1 = self.shot.getAction()[3]
        longShot2 = self.shot.getAction()[4]
        treatmentAct = self.treatment.getAction()[0]

        if self.side == Bornibus.GREEN:
            dispMulti = d3Act
            dispMono = d1Act

        else:
            dispMulti = d2Act
            dispMono = d4Act

        self.action_list = [
            beeAct,
            panelAct,
            dispMono,
            shortShot,
            dispMulti,
            longShot0,
            longShot1,
            longShot2,
            treatmentAct,
        ]

        dispMono.set_reliability(0.6)
        dispMulti.set_reliability(0.6)
        shortShot.set_reliability(0.8)
        longShot0.set_reliability(0.8)
        longShot1.set_reliability(0.8)
        longShot2.set_reliability(0.8)

        treatmentAct.set_impossible_combination(lambda: not (longShot0 or longShot1 or longShot2))
        longShot0.set_predecessors([dispMulti])
        longShot1.set_predecessors([dispMulti])
        longShot2.set_predecessors([dispMulti])
        shortShot.set_predecessors([dispMono])
        longShot0.set_impossible_combination(lambda: longShot1 or longShot2)
        longShot1.set_impossible_combination(lambda: longShot0 or longShot2)
        longShot2.set_impossible_combination(lambda: longShot1 or longShot0)

        self.beacons_receiver = br
        self.beacons_manager = bm

        if self.beacons_manager is not None and self.beacons_receiver is not None:
            self.beacons_manager.create_area(treatmentAct.name, "auxTreatment{}_*".format(self.side))
            self.beacons_manager.create_area(dispMulti.name, "auxDispenser{}_*".format(2 if self.side == Bornibus.GREEN else 3))
            self.beacons_manager.create_area(panelAct.name, "auxSwitch{}_*".format(self.side))

        treatmentAct.link_area(treatmentAct.name)
        dispMulti.link_area(dispMulti.name)
        panelAct.link_area(panelAct.name)

        def longShot(): (not (longShot0 or longShot1 or longShot2))
        dispMulti.set_impossible_combination(lambda: dispMono and not shortShot)
        treatmentAct.set_impossible_combination(lambda: not longShot)
        dispMono.set_impossible_combination(lambda: dispMulti and (not longShot or not treatmentAct))


        #dispMono.set_manual_order(1)
        #shortShot.set_manual_order(2)
        #dispMulti.set_manual_order(3)
        #longShot2.set_manual_order(4)
        longShot0.set_manual_order(4)
        #longShot1.set_manual_order(4)
        #treatmentAct.set_manual_order(5)
        #panelAct.set_manual_order(6)

        self.heuristics = Heuristics(self.action_list, self.arduinos, self.logger, self.beacons_manager,
                                     mode=Heuristics.MANUAL)

    def set_side(self,side):
        self.side = side

    def run(self):
        self.displayManager.start()
        self.logger.reset_time()
        self.arduinos["wheeledbase"].lookahead.set(200)
        self.arduinos["wheeledbase"].max_linvel.set(500)
        self.arduinos["wheeledbase"].max_angvel.set(6)

        self.arduinos["watersorter"].set_shaker_velocity(400)
        self.arduinos["beeActioner"].close()
        self.arduinos["watersorter"].close_trash_unloader()
        self.arduinos["watersorter"].close_trash()

        act = self.heuristics.get_best()
        print(act)
        while act is not None:
            act.before_action()
            self.logger("MAIN : ", "Let's go to the next action : {}".format(act.typ))
            self.mover.goto(*act.actionPoint)
            self.logger("MAIN ; ", "Arrived on action point ! Go execute it =)")
            act()
            act.done = True
            act = self.heuristics.get_best()
            self.mover.reset()

if __name__ == '__main__':
    from robots.setup_bornibus import *
    side = 0
    b.set_position(592, 290, 0)

    print("DEBUT CHARGEMENT ROADMAP")
    geo = Geogebra('bornibus.ggb')
    rm = RoadMap.load(geo)
    print("Fin Chargement")

    br = BaliseReceiver("192.168.1.11")
    #try:
    #    br.connect()
    #except:
    #    pass

    bm = BeaconsManagement(br, "area.ggb")
    bm.start()

    auto = Bornibus(side, rm, geo, b, l, d, ssd, led1, led2, a, s_front, s_lat, s_back, br, bm)
    auto.run()
    exit()