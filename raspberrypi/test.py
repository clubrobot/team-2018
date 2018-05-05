import sys
sys.path.append("{}/common/".format(sys.path[0]))
from serialtalks import *
SWITCH_OPCODE = 0x12
AUTRE_OPCODE = 0x11
arduino = SerialTalks('/dev/ttyACM0')
arduino.connect()

while(True) :
    arduino.send(AUTRE_OPCODE,FLOAT(2.13),LONG(23),FLOAT(62))
    arduino.send(SWITCH_OPCODE,FLOAT(1.2445000410079956),LONG(123456789),FLOAT(3.141592025756836))
