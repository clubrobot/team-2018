import sys
import time
from threading import Thread, RLock, Event

class DisplayPoints:
    def __init__(self, display):
        self.display = display
        self.points = 0
        self.start_time = time.time()
        self.locker = RLock()
        Thread(target=self.run).start()
    
    def addPoints(self, points):
        self.locker.acquire()
        self.points += points
        self.locker.release()

    def updateDisplay(self):
        remaining_time = 100-round(time.time()- self.start_time)
        if remaining_time > 0:
            self.display.set_message("T:"+str(remaining_time)+ "  P:" + str(self.points))
        else:
            self.display.set_message("P:" + str(self.points))

    def run(self):
        while True:
            self.locker.acquire()
            self.updateDisplay()
            self.locker.release()
            time.sleep(0.5)