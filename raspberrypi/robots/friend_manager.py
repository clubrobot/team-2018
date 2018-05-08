from common.tcptalks import *
from robots.get_robot_name import *
from time import sleep
from threading import Thread, Event, Lock

FRIEND_PORT = 11021

FM_GET_POSITION_OPCODE = 0x12
FM_GET_PATH_OPCODE     = 0x13
FM_SET_ACTION          = 0x14

class FriendManager(TCPTalks,Thread):
    def __init__(self, wheeledbase, mover, timestep, logger):
        if ROBOT_ID == BORNIBUS_ID:
            TCPTalks.__init__(self,port=FRIEND_PORT)
        if ROBOT_ID == R128_ID:
            TCPTalks.__init__(self,"192.168.12.1",FRIEND_PORT)

        self.bind(FM_GET_PATH_OPCODE,self._get_path)
        self.bind(FM_SET_ACTION, self._receive_action)
        self.bind(FM_GET_POSITION_OPCODE, self._get_position)
        Thread.__init__(self)

        #Thread things
        self.daemon = True
        self.is_stopped = Event()
        self.is_stopped.clear()
        Thread(target=self.try_connect, daemon=True).start()

        # Action storages
        self.friend_action = "None"
        self.action_did_by_friend = list()
        self.action_lock = Lock()

        # Position storage
        self.friend_position = (0,0)
        self.position_lock = Lock()

        # Intern arguments
        self.wheeledbase = wheeledbase
        self.timestep = timestep
        self.mover = mover
        self.logger = logger


    def _get_position(self):
        return self.wheeledbase.get_position_previous(0.5)[:2]


    def _get_path(self):
        return self.mover.get_path()


    def _receive_action(self, action_id):
        self.action_lock.acquire()
        self.action_did_by_friend.append(self.friend_action)
        self.friend_action = action_id
        self.action_lock.release()


    def launch_action(self, action_id):
        try:
            self.send(FM_SET_ACTION,action_id)
        except:
            return

    def get_friend_action_done(self):
        self.action_lock.acquire()
        result = self.action_did_by_friend + [self.friend_action]
        self.action_lock.release()
        return result



    def get_friend_path(self):
        try:
            return self.execute(FM_GET_PATH_OPCODE)
        except:
            return ((0,0),(0,0))


    def get_friend_position(self):
        self.position_lock.acquire()
        result = self.friend_position
        self.position_lock.release()
        return result

    def run(self):
        while not self.is_stopped.is_set():
            sleep(self.timestep)
            self.position_lock.acquire()
            try:
                self.friend_position = self.execute(FM_GET_POSITION_OPCODE)
            except:
                pass
            self.position_lock.release()

    def try_connect(self):
        connected = False
        while not connected:
            try:
                self.connect(timeout=5)
                self.logger("FRIEND MANAGER : ", "Connected")
                connected = True
            except Exception as e:
                self.logger("FRIEND MANAGER : ", "Not connected" + str(e))
                pass




