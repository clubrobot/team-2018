#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from threading import Thread, Event
from time import sleep
import sys

from common.tcptalks import TCPTalksServer
from beacons.panel import *
from beacons.anchor import *


PORT_BALISE = 26657
GET_POSITION_OPCODE = 0x14
SET_COLOR_OPCODE    = 0x15
BIG_ROBOT = 0
LITTLE_ROBOT = 1

class Server(Thread, TCPTalksServer):
	def __init__(self):
		TCPTalksServer.__init__(self,PORT_BALISE)
		Thread.__init__(self)
		self.bind(GET_POSITION_OPCODE, self.getPosition)
        	#self.panel = Panel()
		self.beacon = Anchor()
		self.beacon.connect()

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

	def  setSide(self,side):
		try:
			self.beacon.update_color(side)
		except:
			pass

	def getPosition(self, id):
		print(id)
		if id ==0 :
			try:
				return	self.beacon.get_position()
			except:
				return (-1000,-1000)

		return (-1000,-1000)
