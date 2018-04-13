#!/usr/bin/env python3
# coding: utf-8
import sys
sys.path.append("../../common/")
from tcptalks import TCPTalks

BIG_ROBOT    = 0
LITTLE_ROBOT = 1

GET_POSITION_OPCODE = 0x10
GET_ANGLE_OPCODE    = 0x15
GET_VELOCITY_OPCODE = 0x20

class BaliseReceiver(TCPTalks):

    def __init__(self,ip=None, port=25565,id=None, password=None):
        TCPTalks.__init__(self,ip, port,id, password)

    def get_position(self,robotID):
        return self.execute(GET_POSITION_OPCODE,robotID)

    def get_velocity(self,robotID):
        return self.execute(GET_VELOCITY_OPCODE,robotID)

    def get_angle(self,robotID):
        return self.execute(GET_ANGLE_OPCODE,robotID)


