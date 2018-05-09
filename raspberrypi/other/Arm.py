import time
from math import pi


from common.components         import *
from common.serialtalks        import *
from arduino.RobotArm 		   import *


CUBE1 = ()

try:
	r = RobotArm()
	r.connect()
except:
	print('\'RobotArm\' not connected')


r.begin()

time.sleep(3)

r.set_pos(-26.5,3,10,270,1);
time.sleep(1)
r.open_gripper()

time.sleep(3)

r.set_z(0)
time.sleep(2)
r.close_gripper()
time.sleep(2)
r.set_z(10)

r.set_theta(0)

time.sleep(1)

r.set_theta(-20)

time.sleep(1)

r.set_speed(100)

r.set_pos(0,12,10,2,1)
time.sleep(3)
r.set_pos(8,16,10,2,1)
time.sleep(1)
r.set_pos(11,17.9,10,2,1)
time.sleep(1)
r.set_pos(13,18.9,10,2,1)

#r.set_speed(50)
time.sleep(3)
r.set_z(2)
time.sleep(3)
r.open_gripper()
time.sleep(3)
r.set_z(10)

r.set_speed(500)
time.sleep(3)

r.set_pos(8,16,10,2,1)

# time.sleep(3)

# r.set_z(0)
# time.sleep(2)
# r.open_gripper()
# time.sleep(2)
# r.set_z(10)

# #*****************************

# time.sleep(3)

# r.set_pos(-17.5,6,10,180,1);
# r.open_gripper()

# time.sleep(3)

# r.set_z(0)
# time.sleep(2)
# r.close_gripper()
# time.sleep(2)
# r.set_z(10)

# r.set_theta(0)

# time.sleep(1)

# r.set_pos(25,5,10,0,1);

# time.sleep(3)

# r.set_z(7)
# time.sleep(2)
# r.open_gripper()
# time.sleep(2)
# r.set_z(10)

# time.sleep(3)
# #*****************************

# r.set_pos(-22.5,0,10,90,1);
# r.open_gripper()

# time.sleep(3)

# r.set_z(0)
# time.sleep(2)
# r.close_gripper()
# time.sleep(2)
# r.set_z(10)

# r.set_theta(0)

# time.sleep(1)

# r.set_pos(25,5,15,0,1);

# time.sleep(3)

# r.set_z(14)
# time.sleep(2)
# r.open_gripper()
# time.sleep(2)
# r.set_z(18)

# #*****************************
# time.sleep(3)

# r.set_pos(-23.5,7,20,180,1);
# r.open_gripper()

# time.sleep(3)

# r.set_z(0)
# time.sleep(2)
# r.close_gripper()
# time.sleep(2)
# r.set_z(21)

# r.set_theta(0)

# time.sleep(1)

# r.set_pos(25,5,20,0,1);

# time.sleep(3)

# r.set_z(20)
# time.sleep(2)
# r.open_gripper()
# time.sleep(2)

