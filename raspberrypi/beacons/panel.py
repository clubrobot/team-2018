#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from common.tcptalks import TCPTalks, TCPListener, AlreadyConnectedError
from threading import Thread, Event
from time import sleep
PING_OPCODE = 0x10
#TODO AJOUTER l'OPCODE
PORT = 26656

class Panel(Thread):
    def __init__(self, timestep=1, fail_accept = 3):
        Thread.__init__(self)
        self.deamond = True
        self.fail_accept = fail_accept
        self.timestep = timestep
        self.core = TCPTalks(port=PORT)
        self.connected  = Event()
        self.is_running = Event()
        self.trying_attempt = 0

    def is_connected(self):
        return self.connected.is_set()

    def stop(self):
        self.is_running.set()

    def run(self):
        while not self.is_running.is_set():
            if self.connected.is_set():
                try:
                    self.core.execute(PING_OPCODE,timeout=1)
                    self.trying_attempt= 0
                    sleep(self.timestep)
                except Exception:
                    self.trying_attempt +=1
                    if self.trying_attempt>self.fail_accept:
                        print("DISCONNECTED")
                        self.trying_attempt = 0
                        self.core.disconnect()
                        self.connected.clear()
            else:
                try:
                    self.core.connect(timeout=2)
                    print("CONNECTED")
                    self.connected.set()

                except AlreadyConnectedError:
                    print("CONNECTED")
                    self.connected.set()
                except TimeoutError or ConnectionError:
                    pass

