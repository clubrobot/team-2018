#!/usr/bin/env python3
# coding: utf-8
import sys
sys.path.append("../../common/")
from tcptalks import TCPTalks

BIG_ROBOT    = 0
LITTLE_ROBOT = 1

GET_POSITION_OPCODE = 0x14
SET_COLOR_OPCODE    = 0x15
PORT_BALISE = 26657

class BaliseReceiver(TCPTalks):

    def __init__(self,ip=None, port=PORT_BALISE,id=None, password=None):
        TCPTalks.__init__(self,ip =ip,port= port)

    def get_position(self,robotID):
        try:
            output =  self.execute(GET_POSITION_OPCODE,robotID)
        except:
            return (-1000,-1000)
        return output

    def set_color(self,color):
        self.send(SET_COLOR_OPCODE, color)

#    def get_velocity(self,robotID):
#        return self.execute(GET_VELOCITY_OPCODE,robotID)
#
#    def get_angle(self,robotID):
#        return self.execute(GET_ANGLE_OPCODE,robotID)


