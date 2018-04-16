from setup_bornibus import *

d.close_outdoor()
d.open_indoor()
d.disable_shaker()
d.write_trash(126)
l.set_motor_velocity(0)