#!/usr/bin/env python3
# coding: utf-8

import math
import time

from setup_bornibus import *

class Shot:
    def realize_without_sort(self, watersorter, waterlauncher, global_timeout=210):
        nb_balls = 0
        begin_time = time.time()
        motor_base = 81
        timeout_per_ball_in = 1
        timeout_per_ball_out = 2
        currentPosXY=wheeledbase.get_position()[:2]
        waterlauncher.set_motor_pulsewidth(1000 + motor_base)

        watersorter.enable_shaker_equal()
        time.sleep(1)

        waterlauncher.get_nb_launched_water()
        while nb_balls < 8 and time.time() - begin_time < global_timeout:
            print("SHOT : ", "Ball N°", nb_balls+1)
            if not (time.time() - begin_time > global_timeout):
                print("SHOT : ", "Waiting ball in sorter")
                open_time = time.time()
                while not (watersorter.get_water_color()[0] > 100 or watersorter.get_water_color()[1]>100) and not (time.time() - begin_time > global_timeout):
                    time.sleep(0.1)
                    if time.time() - open_time > timeout_per_ball_in:
                        watersorter.close_trash()
                        open_time = time.time()
               
            time.sleep(0.2)
            watersorter.open_outdoor()
            watersorter.close_indoor()

            if not (time.time() - begin_time > global_timeout):
                print("SHOT : ", "Launching ball")
                close_time = time.time()
                while waterlauncher.get_nb_launched_water() < 1 and not (time.time() - begin_time > global_timeout):
                    time.sleep(0.1)
                    waterlauncher.set_motor_pulsewidth(1000+motor_base)
                    if time.time() - close_time > timeout_per_ball_out:
                        watersorter.close_trash()
                        close_time = time.time()
                         
              
            if time.time() - begin_time < global_timeout:
                nb_balls += 1
#                display.addPoints(Shot.POINTS_PER_BALL_CASTLE)
#                display.happy(1)
                print("SHOT : ", "Ball Launched")
            else:
                print("SHOT : ", "TIMEOUT")

            waterlauncher.set_motor_pulsewidth(1150)
            time.sleep(0.1)
            waterlauncher.set_motor_pulsewidth(1000 + motor_base)
            watersorter.open_indoor()
            watersorter.close_outdoor()
            time.sleep(0.4)

        watersorter.disable_shaker()
        wheeledbase.angpos_threshold.set(old)
        waterlauncher.set_motor_velocity(0)
        watersorter.close_outdoor()
        watersorter.open_indoor()

Shot.realize_without_sort(None, watersorter, waterlauncher)
