from common.tcptalks import *
from robots.get_robot_name import *
from time import sleep

FRIEND_PORT = 11021


class FriendManager(TCPTalks,Thread):
    def __init__(self, wheeledbase, mover, timestep ):
        if ROBOT_ID == BORNIBUS:
            TCPTalks.__init__(self,FRIEND_PORT)
        if ROBOT_ID == R128:
            TCPTalks.__init__(self,"192.168.12.1",FRIEND_PORT)
        Thread.__init__(self)
        self.connect(timeout=10)

        self.wheeledbase = wheeledbase
        self.timestep = timestep
        self.friend_action = None
        self.own_action = None
        self.friend_position = (0,0)
        self.action_did_by_friend = list()
        self.is_stopped = Event()
        self.is_stopped.clear()
        self.mover = mover
        self.action_lock = Lock()
        self.

    def _get_position(self):
        return self.wheeledbase.get_position()[:2]

    def _get_action(self):
        return self.own_action

    def _get_path(self):
        return self.mover.get_path()


    def set_action(self):



    def run(self):
        while not self.is_stopped.is_set():
            sleep(self.timestep)



