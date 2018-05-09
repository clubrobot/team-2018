from robots.cubes_manager        import CubeManagement, Cross
from robots.display_manager      import DisplayPoints
from robots.mover                import Mover, PositionUnreachable
from robots.heuristics           import Heuristics
from common.logger               import Logger
from robots.beacons_manager      import BeaconsManagement
from beacons.balise_receiver     import BaliseReceiver
from robots.switch_manager_128       import Interrupteur_128, Abeille_128, Odometry
from robots.get_robot_name import *
from robots.friend_manager import FriendManager
import time
if ROBOT_ID == R128_ID:
    from robots.color_pattern import Pattern


class R128:
    cube ="cube"
    dispenser = "disp"
    shot = "shot"
    GREEN  = 0
    ORANGE = 1
    def __init__(self, side, roadmap, geogebra, wheeledbase, display, led1, led2, beeActioner, robot_arm, sensors_front, sensors_lat, sensors_back, br, bm, p):
        # Save arduinos
        self.arduinos = dict(wheeledbase=wheeledbase,
                             display=display,
                             beeActioner=beeActioner,
                             sensors_front=sensors_front,
                             sensors_lat=sensors_lat,
                             sensors_back=sensors_back,
                             robot_arm=robot_arm,
                             )


        # Save annexes inf
        self.side     = side
        self.pattern = p
        self.roadmap  = roadmap
        self.geogebra = geogebra
        self.logger   = Logger(Logger.SHOW)
        robot_arm.set_logger(self.logger)
        self.mover    = Mover(side, roadmap, self.arduinos, self.logger, br)
        self.friend = self.mover.get_friend()
        self.beacons_receiver = br
        self.beacons_manager = bm
        self.data = dict()
        self.displayManager = DisplayPoints(display, led1, led2)

    def set_side(self, side):
        self.side = side
        # Apply cube obstacle
        self.cube_management = CubeManagement(self.roadmap, self.geogebra)

        self.bee = Abeille_128(self.side, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger,
                           self.data)
        self.panel = Interrupteur_128(self.side, self.geogebra, self.arduinos, self.displayManager, self.mover, self.logger,
                                  self.beacons_receiver, self.data)

        self.odometry = Odometry(self.side, self.geogebra, self.arduinos, self.mover, self.logger, self.data)
        self.odoAct  =self.odometry.getAction()[0]
        self.action_list = []
        self.cross = []
        self.cross = Cross(self.side, 1, self.roadmap, self.geogebra, self.arduinos, self.mover, self.logger, self.data)
        self.crossAct = self.cross.getAction()[0]

        self.beeAct = self.bee.getAction()[0]
        self.panelAct = self.panel.getAction()[0]

        self.action_list = [
            self.beeAct,
            self.panelAct,
            self.odoAct,
            self.crossAct,
        ]

        #self.odoAct.set_manual_order(1)
        #self.beeAct.set_manual_order(3)
        self.panelAct.set_manual_order(2)
        self.crossAct.set_manual_order(2)

        self.heuristics = Heuristics(self.action_list, self.arduinos, self.logger, self.beacons_manager, self.friend,
                                     mode=Heuristics.MANUAL)
        if self.side == R128.GREEN:
            self.arduinos["wheeledbase"].set_position(510, 270, 0)
        else:
            self.arduinos["wheeledbase"].set_position(510, 3000-270, 0)

    def run(self):
        self.displayManager.start()
        self.logger.reset_time()
        self.mover.reset()

        act = self.heuristics.get_best()
        self.arduinos["robot_arm"].begin()
        time.sleep(2)
        print(act)
        while act is not None:
            try:
                act.before_action()
                self.logger("MAIN : ", "Let's go to the next action : {}".format(act.name))
                self.mover.goto(*act.actionPoint)
                self.logger("MAIN ; ", "Arrived on action point ! Go execute it =)")
                act()
                act.done.set()
            except PositionUnreachable:
                act.temp_disable(5)

            act = self.heuristics.get_best()
            self.mover.reset()


if __name__ == '__main__':
    from robots.setup_128 import *

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
    if ROBOT_ID == R128:
        p = Pattern()
    else:
        p = None
    auto = R128(0, rm, geo, wheeledbase, ssd, led1, led2, beeactuator, arm, s_front, s_lat, s_back, br, bm, p)
    auto.set_side(0)
    auto.run()
