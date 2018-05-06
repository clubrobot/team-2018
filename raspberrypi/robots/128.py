from robots.cubes_manager        import CubeManagement, Cross
from robots.display_manager      import DisplayPoints
from robots.mover                import Mover
from robots.heuristics           import Heuristics
from common.logger               import Logger
from robots.beacons_manager      import BeaconsManagement
from beacons.balise_receiver     import BaliseReceiver
from robots.switch_manager_128       import Interrupteur, Abeille

class R128:
    def __init__(self, side, roadmap, geogebra, wheeledbase, display, led1, led2, beeActioner,sensors_front, sensors_lat, sensors_back, br, bm):
        # Save arduinos
        self.arduinos = dict(wheeledbase=wheeledbase,
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
        self.beacons_receiver = br
        self.beacons_manager = bm
        self.data = dict()

        # Apply cube obstacle
        self.cube_management = CubeManagement(self.roadmap, self.geogebra)

        self.bee   = Abeille(self.side, self.geogebra,  self.arduinos, self.displayManager, self.mover, self.logger, self.data)
        self.panel = Interrupteur(self.side, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger, self.beacons_receiver, self.data)

        self.action_list = []
        self.cross = []
        self.cross = Cross(self.side, 1,self.roadmap, self.geogebra, self.arduinos, self.mover, self.logger, self.data)
        self.action_list += self.cross.getAction()

        self.heuristics = Heuristics(self.action_list, self.arduinos, self.logger, self.beacons_manager,
                                     mode=Heuristics.AUTO)

    def run(self):
        self.logger.reset_time()
        self.mover.reset()

        act = self.heuristics.get_best()
        print(act)
        while act is not None:
            act.before_action()
            self.logger("MAIN : ", "Let's go to the next action : {}".format(act.name))
            self.mover.goto(*act.actionPoint)
            self.logger("MAIN ; ", "Arrived on action point ! Go execute it =)")
            act()
            act.done.set()
            act = self.heuristics.get_best()
            self.mover.reset()


if __name__ == '__main__':
    from robots.setup_128 import *
    side = 1
    wheeledbase.set_position(510, 3000-270, 0)

    print("DEBUT CHARGEMENT ROADMAP")
    geo = Geogebra('128.ggb')
    rm = RoadMap.load(geo)
    print("Fin Chargement")

    br = BaliseReceiver("192.168.12.3")
   # try:
   #     br.connect()
   # except:
   #     print("BALISE : Not connected")
   #     pass

    bm = BeaconsManagement(br, "area.ggb")

    auto = R128(side, rm, geo, wheeledbase, ssd, led1, led2, beeactuator, s_front, s_lat, s_back, br, bm)
    auto.run()
