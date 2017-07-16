#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import math

from serialtalks import BYTE, INT, LONG, FLOAT
from components import SerialTalksProxy
from threading import RLock

# Instructions

_SET_ROLLER_VELOCITY_OPCODE 		=	0x03
_SET_FIRING_HAMMER_VELOCITY_OPCODE	=	0x04
_RETURN_TO_SAFE_POSITION_OPCODE		= 	0x0B
_SETUP_AX_OPCODE					=	0x0C
_SET_AX_POSITION_OPCODE				=	0X05
_GET_AX_POSITION_OPCODE				=	0X06
_GET_AX_TORQUE_OPCODE				=	0X07
_SET_AX_VELOCITY_MOVE_OPCODE		=	0X08
_PING_AX_OPCODE						=	0x09
_SET_AX_HOLD_OPCODE					=	0X0A
_GET_AX_VELOCITY_OPCODE				=	0x10
_GET_AX_MOVING_OPCODE				=	0x0D

AX12_SEND_INSTRUCTION_PACKET_OPCODE = 0x0E
AX12_RECEIVE_STATUS_PACKET_OPCODE   = 0x0F

LAUNCHPAD_SET_POSITION_OPCODE 		=	0x11

proxy_locks_array = dict()

def thread_safe_send(proxy, *args, **kwargs):
	if not proxy._compid in proxy_locks_array:
		proxy_locks_array[proxy._compid] = RLock()
	lock = proxy_locks_array[proxy._compid]
	lock.acquire()
	try: return proxy.send(*args, **kwargs) 
	except: raise
	finally: lock.release()

def thread_safe_execute(proxy, *args, **kwargs):
	if not proxy._compid in proxy_locks_array:
		proxy_locks_array[proxy._compid] = RLock()
	lock = proxy_locks_array[proxy._compid]
	lock.acquire()
	try: return proxy.execute(*args, **kwargs) 
	except: raise
	finally: lock.release()

class AX12(SerialTalksProxy):	
	def __init__(self, parent, uuid='mineralscollector'):
		SerialTalksProxy.__init__(self, parent, uuid)		
		self.closed_position = 300
		self.gathering_position = 80
		self.entry_position = 105
		self.storage_position = 285
		self.ax_velocity = 300
		thread_safe_execute(self, _SETUP_AX_OPCODE)

	def set_position(self, a):
		thread_safe_execute(self, _SET_AX_POSITION_OPCODE, FLOAT(a))

	def get_position(self):
		output = thread_safe_execute(self, _GET_AX_POSITION_OPCODE)
		pos = output.read(FLOAT)
		return float(pos)
	
	def get_torque(self):
		output = thread_safe_execute(self, _GET_AX_TORQUE_OPCODE)
		trq = output.read(INT)
		return int(trq)
	
	def set_position_velocity(self, p, v):
		thread_safe_execute(self, _SET_AX_VELOCITY_MOVE_OPCODE, FLOAT(p), INT(v))
	
	def ping(self):
		output = thread_safe_execute(self, _PING_AX_OPCODE)
		ping = output.read(INT)
		return int(ping)
	
	def hold(self, i):
		thread_safe_execute(self, _SET_AX_HOLD_OPCODE, INT(i))

	def goto(self, pos, vel=None, threshold=15, timeout=3):
		if vel is not None:
			self.set_position_velocity(pos, vel)
		else:
			self.set_position(pos)
		startingtime = time.monotonic()
		while abs(self.get_position() - pos) > threshold:
			time.sleep(0.1)
			if timeout is not None and time.monotonic() - startingtime > timeout:
				raise RuntimeError("can't reach position")

	def gather(self):
		self.goto(self.gathering_position, self.ax_velocity)

	def store(self):
		self.goto(self.storage_position, self.ax_velocity)

	def enter(self):
		self.goto(self.entry_position, self.ax_velocity)
	
	def close(self):
		self.goto(self.closed_position, self.ax_velocity)

	def set_closed_position(self, a):
		self.closed_position = a
	
	def set_gathering_position(self, a):
		self.gathering_position = a

	def set_entry_position(self, a):
		self.entry_position = a

	def set_storage_position(self, a):
		self.storage_position = a

	def send_instruction_packet(self, packet):
		thread_safe_send(self, AX12_SEND_INSTRUCTION_PACKET_OPCODE, BYTE(len(packet)), *map(BYTE, packet))

	def receive_status_packet(self):
		output = self.execute(AX12_RECEIVE_STATUS_PACKET_OPCODE)
		packet = []
		for i in range(output.read(BYTE)):
			packet.append(output.read(BYTE))
		return packet

	def read_data(self, address, length=1):
		self.receive_status_packet() # Purge status packets
		content = [0x02, 0x04, 0x02, address, length]
		checksum = ~sum(content) & 0xFF
		packet = [0xFF, 0xFF] + content + [checksum]
		self.send_instruction_packet(self, packet)
		time.sleep(0.1)
		return self.receive_status_packet()[5:-1]

	def write_data(self, address, data):
		content = [0x02, 3 + len(data), 0x03, address] + data
		checksum = ~sum(content) & 0xFF
		packet = [0xFF, 0xFF] + content + [checksum]
		self.send_instruction_packet(self, packet)
	
	def get_velocity(self):
		output = thread_safe_execute(self, _GET_AX_VELOCITY_OPCODE)
		vel = output.read(INT)
		return int(vel)
	
	def is_Moving(self):
		output = thread_safe_execute(self, _GET_AX_MOVING_OPCODE)
		mov = output.read(INT)
		time.sleep(0.1)
		return int(mov)


class Hammer(SerialTalksProxy):
	def __init__(self, parent, uuid='mineralscollector'):
		SerialTalksProxy.__init__(self, parent, uuid)
		self.firing_velocity = 11	

	def set_velocity(self, a):
		thread_safe_send(self, _SET_FIRING_HAMMER_VELOCITY_OPCODE, FLOAT(a))

	def fire(self):
		self.set_velocity(self.firing_velocity)
	
	def stop(self):
		self.set_velocity(0)

	def move_to_safe_position(self):
		thread_safe_send(self, _RETURN_TO_SAFE_POSITION_OPCODE)

class Roller(SerialTalksProxy):
	def __init__(self, parent, uuid='mineralscollector'):
		SerialTalksProxy.__init__(self, parent, uuid)
		self.gathering_velocity = 8
		self.storage_velocity = 3

	def set_velocity(self, a):
		thread_safe_send(self, _SET_ROLLER_VELOCITY_OPCODE, FLOAT(a))

	def gather(self):
		self.set_velocity(self.gathering_velocity)
	
	def storage(self):
		self.set_velocity(self.storage_velocity)

	def stop(self):
		self.set_velocity(0)


class LaunchPad(SerialTalksProxy):
	def __init__(self, parent, uuid='mineralscollector'):
		SerialTalksProxy.__init__(self, parent, uuid)
		self.launch_position = 60
		self.hold_position = 159

	def set_position(self, pos):
		thread_safe_send(self, LAUNCHPAD_SET_POSITION_OPCODE, INT(pos))

	def launch(self):
		self.set_position(self.launch_position)
	
	def hold(self):
		self.set_position(self.hold_position)
