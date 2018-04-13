#!/usr/bin/env python3

import os, sys
import time
from argparse  import ArgumentParser
from threading import Thread

sys.path.append("{}/common/".format(sys.path[0]))

from serialtalks import SerialTalks
from tcptalks import Server





server_parser = subparsers.add_parser('server')
server_parser.set_defaults(func=server)


args = parser.parse_args()
args.func(args)


