#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
sys.path.append("../common/")

import time
import math

from serialtalks import *
from components import SerialTalksProxy

# Instructions

GET_POSITION_OPCODE  = 0x10


class tag(SerialTalksProxy):

	def __init__(self, parent, uuid='tag'):
		SerialTalksProxy.__init__(self, parent, uuid)

	def get_position(self, **kwargs):
		output = self.execute(GET_POSITION_OPCODE, **kwargs)
		x, y = output.read(FLOAT, FLOAT)
		return x, y
	

