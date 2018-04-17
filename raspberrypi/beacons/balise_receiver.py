#!/usr/bin/env python3
# coding: utf-8

from common.tcptalks import TCPTalks

BIG_ROBOT = 0
LITTLE_ROBOT = 1

GET_POSITION_OPCODE = 0x14
SET_COLOR_OPCODE = 0x15
PORT_BALISE = 26657


class BaliseReceiver(TCPTalks):

    def __init__(self, ip=None, port=PORT_BALISE, password=None):
        TCPTalks.__init__(self, ip=ip, port=port)

    def get_position(self, robotID):
        try:
            output = self.execute(GET_POSITION_OPCODE, robotID)
        except:
            return (-1000, -1000)
        return output

    def set_color(self, color):
        self.send(SET_COLOR_OPCODE, color)