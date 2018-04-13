import sys
sys.path.append("../common/")

from tcptalks import TCPTalksServer
from threading import Thread, Event
from time import sleep
from panel import *

PORT_BALISE = 26657
GET_POSITION_OPCODE = 0x14
BIG_ROBOT = 0
LITTLE_ROBOT = 1

class Server(Thread, TCPTalksServer):
    def __init__(self):
        TCPTalksServer.__init__(self,PORT_BALISE)
        Thread.__init__(self)
        self.bind(GET_POSITION_OPCODE, self.getPosition)
        #self.panel = Panel()
        #self.beacon = Beacon() 
    
    def run(self):
        while True:
            try:
                while not self.full():
                    self.connect(timeout=100)
                self.sleep_until_one_disconnected()

            except KeyboardInterrupt:
                break
            except Exception as e:
                sys.stderr.write('{}: {}\n'.format(type(e).__name__, e))
                continue

    def getPosition(self, client, id):
        return (1000,1000)

