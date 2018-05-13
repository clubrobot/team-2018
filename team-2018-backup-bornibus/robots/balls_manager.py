#!/usr/bin/env python3
# coding: utf-8

import math
import time

from robots.automateTools import AutomateTools
from robots.action import Action, Actionnable
from robots.mover import Mover, PositionUnreachable

class Dispenser(Actionnable):
    typ="Dispenser"
    POINTS_DISPENSER = 10
    TIME = 15
    def __init__(self,numberDispenser, rm, geo, arduinos, display, mover, logger, data):
        self.rm  = rm
        self.geo = geo
        self.mover = mover
        self.logger = logger
        self.display = display
        self.numberDispenser=numberDispenser
        self.watersorter = arduinos["watersorter"]
        self.wheeledbase = arduinos["wheeledbase"]
        self.waterlauncher = arduinos["waterlauncher"]
        self.targetPoint=self.geo.get('Dispenser'+str(self.numberDispenser)+'_1')
        self.preparationPoint=self.geo.get('Dispenser'+str(self.numberDispenser)+'_0')
        self.data = data

    def realize(self,robot ,watersorter ,display):
        theta = math.atan2(self.preparationPoint[1]-self.targetPoint[1],self.preparationPoint[0]-self.targetPoint[0])+3.141592
        robot.max_linvel.set(300)
        robot.max_angvel.set(3)
        watersorter.close_trash()
        watersorter.close_outdoor()
        watersorter.open_indoor()
        self.logger("DISPENSER : ", " Aim the dispenser !")
        self.display.sleep()
        robot.turnonthespot(theta)
        self.mover.turnonthespot(theta, 3, Mover.AIM)
        path = [self.preparationPoint,self.targetPoint]
        self.logger("DISPENSER : "," Let's go to the rumble !")
        self.display.angry(1)
        robot.purepursuit(path,direction='forward')
        robot.max_linvel.set(500)
        robot.max_angvel.set(6)
        self.watersorter.enable_shaker_diff()
        time.sleep(0.2)
        init_pos = (0,0)
        try:
            robot.wait()
        except RuntimeError:
            init_pos = robot.get_position()[:-1]
            display.addPoints(Dispenser.POINTS_DISPENSER)
            self.display.sick(3)
            self.logger("DISPENSER : ", "CONTACT !! Just try to take balls here {},{}", *init_pos)
            begin = time.time()
            while time.time() - begin < 2:
                self.wheeledbase.set_velocities(-150, 2)
                time.sleep(0.4)
                self.wheeledbase.set_velocities(200, -2)
                time.sleep(0.4)

        self.logger("DISPENSER : ", "Trying to go backward ")
        pos = robot.get_position()[:-1]
        self.mover.withdraw(*self.preparationPoint, direction="backward", timeout=5, strategy=Mover.HARD,
                            last_point_aim=self.targetPoint)
        self.watersorter.disable_shaker()
        robot.stop()
        self.display.happy(2)
        

        
    def getAction(self):
        return [Action( self.preparationPoint,
                        lambda : self.realize(self.wheeledbase,self.watersorter, self.display),
                        Dispenser.typ, 
                        "DISPENSER"+str(self.numberDispenser),
                        Dispenser.POINTS_DISPENSER,
                        Dispenser.TIME)]


class Shot(Actionnable):
    typ="shot"
    POINTS_PER_BALL_CASTLE = 5
    POINTS_PER_BALL_EPURATION = 10
    TIME_SORTED = 30
    TIME_UNSORTED = 20
    def __init__(self, side, rm, geo, arduinos, display, mover, logger, data):
        self.side=side
        self.rm  = rm
        self.geo = geo
        self.mover  = mover
        self.logger = logger
        self.wheeledbase = arduinos["wheeledbase"]
        self.watersorter = arduinos["watersorter"]
        self.waterlauncher = arduinos["waterlauncher"]
        self.display = display
        self.shootCastlePoint=self.geo.get('ShootCastle'+str(self.side))
        self.shootCastlePointLong0=self.geo.get('ShootCastleLong'+str(self.side)+'_0')
        self.shootCastlePointLong1=self.geo.get('ShootCastleLong'+str(self.side)+'_1')
        self.shootCastlePointLong2=self.geo.get('ShootCastleLong'+str(self.side)+'_2')
        self.castlePoint=self.geo.get('Castle'+str(self.side))
        self.data = data
        
        
    def realize_without_sort(self, wheeledbase, watersorter, waterlauncher, display, global_timeout=16):
        nb_balls = 0
        begin_time = time.time()
        motor_base = 81
        timeout_per_ball_in = 1
        timeout_per_ball_out = 1
        currentPosXY=wheeledbase.get_position()[:2]
        waterlauncher.set_motor_pulsewidth(1000 + motor_base)
        theta = math.atan2(self.castlePoint[1]-currentPosXY[1],self.castlePoint[0]-currentPosXY[0])
        try:
            wheeledbase.angpos_threshold.set(0.05)
            self.mover.turnonthespot(theta, 3, Mover.AIM)

        except PositionUnreachable:
            wheeledbase.angpos_threshold.set(0.1)
            return
        old = wheeledbase.angpos_threshold.get()
        wheeledbase.angpos_threshold.set(0.1)
        watersorter.enable_shaker_equal()
        time.sleep(0.2)

        waterlauncher.get_nb_launched_water()
        while nb_balls < 8 and time.time() - begin_time < global_timeout:
            self.logger("SHOT : ", "Ball N°", nb_balls+1)
            if not (watersorter.get_water_color()[0] > 100 or watersorter.get_water_color()[1] > 100):
                watersorter.open_indoor()
                watersorter.close_trash()
                self.logger("SHOT : No ball in sorter")
            else:
                self.logger("Shot : already ball in sorter")

            watersorter.close_outdoor()

            if not (time.time() - begin_time > global_timeout):
                self.logger("SHOT : ", "Waiting ball in sorter")
                open_time = time.time()
                while not (watersorter.get_water_color()[0] > 100 or watersorter.get_water_color()[1]>100) and not (time.time() - begin_time > global_timeout):
                    time.sleep(0.1)
                    if time.time() - open_time > timeout_per_ball_in:
                        watersorter.close_trash()
                        open_time = time.time()

            time.sleep(0.4)
            watersorter.open_outdoor()
            watersorter.close_indoor()

            if not (time.time() - begin_time > global_timeout):
                self.logger("SHOT : ", "Launching ball")
                close_time = time.time()
                while waterlauncher.get_nb_launched_water() < 1 and not (time.time() - begin_time > global_timeout):
                    time.sleep(0.1)
                    waterlauncher.set_motor_pulsewidth(1000+motor_base)
                    if time.time() - close_time > timeout_per_ball_out:
                        watersorter.close_trash()
                        break

            if time.time() - begin_time < global_timeout:
                nb_balls += 1
                display.addPoints(Shot.POINTS_PER_BALL_CASTLE)
                display.happy(1)
                self.logger("SHOT : ", "Ball Launched")
            else:
                self.logger("SHOT : ", "TIMEOUT")

            waterlauncher.set_motor_pulsewidth(1150)
            time.sleep(0.2)
            waterlauncher.set_motor_pulsewidth(1000 + motor_base)

        watersorter.disable_shaker()
        wheeledbase.angpos_threshold.set(old)
        waterlauncher.set_motor_velocity(0)
        watersorter.close_outdoor()
        watersorter.open_indoor()
            
    def realize_with_sort(self,wheeledbase, watersorter, waterlauncher, display, global_timeout=20):
        motor_base = 107
        waterlauncher.set_motor_pulsewidth(1000 + motor_base)
        currentPosXY=wheeledbase.get_position()[:2]
        theta = math.atan2(self.castlePoint[1]-currentPosXY[1],self.castlePoint[0]-currentPosXY[0])
        try:
            wheeledbase.angpos_threshold.set(0.05)
            self.mover.turnonthespot(theta, 3, Mover.AIM)
        except PositionUnreachable:
            wheeledbase.angpos_threshold.set(0.1)
            return
        old = wheeledbase.angpos_threshold.get()
        wheeledbase.angpos_threshold.set(0.1)
        watersorter.enable_shaker_equal()
        time.sleep(0.2)
        watersorter.close_indoor()
        watersorter.close_trash_unloader()
        watersorter.close_outdoor()
        waterlauncher.get_nb_launched_water()
        nb_ball = 0
        begin_time = time.time()
        timeout_per_ball_in = 1
        timeout_per_ball_out = 1

        CASTLE = 0
        TREATMENT = 1

        while not (time.time() - begin_time > global_timeout) and nb_ball<8:
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            if not (watersorter.get_water_color()[0] > 100 or watersorter.get_water_color()[1] > 100):
                watersorter.open_indoor()
                watersorter.close_trash()
                self.logger("SHOT : No ball in sorter")
            else:
                self.logger("Shot : already ball in sorter")

            watersorter.close_outdoor()

            if not (time.time() - begin_time > global_timeout):
                self.logger("SHOT : ", "Waiting ball in sorter")
                open_time = time.time()
                while not (watersorter.get_water_color()[0] > 100 or watersorter.get_water_color()[1]>100) and not (time.time() - begin_time > global_timeout):
                    time.sleep(0.1)
                    if time.time() - open_time > timeout_per_ball_in:
                        watersorter.close_trash()
                        open_time = time.time()

            time.sleep(0.4)

            #Verification de la sortie dans le canon
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            watersorter.close_indoor()
            nb_ball+=1
            # On verifie si la code couleur est bon
            if not (time.time() - begin_time > global_timeout):
                if watersorter.get_water_color()[0] < watersorter.get_water_color()[1] and not (time.time() - begin_time > global_timeout):
                    self.logger("SHOT : ", "Green ball")
                    if self.side==0:
                        action = CASTLE
                    else:
                        action = TREATMENT
                elif not (time.time() - begin_time > global_timeout):
                    self.logger("SHOT : ", "Orange ball")
                    if self.side==0:
                        action = TREATMENT
                    else:
                        action = CASTLE

            if not (time.time() - begin_time > global_timeout):
                if action == CASTLE:
                    self.logger("SHOT : ", "Castle")
                    watersorter.open_outdoor()
                    display.happy(1)
                    close_time = time.time()
                    while waterlauncher.get_nb_launched_water() < 1 and not (time.time() - begin_time > global_timeout):
                        self.logger("SHOT : ", "En attente de la sortie ")
                        if time.time() - close_time > timeout_per_ball_out:
                            watersorter.close_trash()
                            break
                        time.sleep(0.1)
                    waterlauncher.set_motor_pulsewidth(1200)
                    time.sleep(0.1)
                    waterlauncher.set_motor_pulsewidth(1000 + motor_base)
                    display.addPoints(Shot.POINTS_PER_BALL_CASTLE)
                    time.sleep(0.2)

                else:
                    self.logger("SHOT : ", "Treatment")
                    watersorter.open_trash()
                    time.sleep(0.1)
                    watersorter.open_outdoor()
                    display.sleep(1)
                    while (watersorter.get_water_color()[0]>80 or watersorter.get_water_color()[1]>80) and not (time.time() - begin_time > global_timeout):
                        time.sleep(0.1)
                        self.logger("SHOT : ", "En attente de la sortie")
                    time.sleep(0.6)
                    self.data["nb_balls_in_unloader"] += 1

            if time.time() - begin_time > global_timeout:
                self.logger("SHOT : ", "TIMEOUT")

        watersorter.open_indoor()
        watersorter.close_trash()
        watersorter.close_outdoor()
        watersorter.disable_shaker()
        wheeledbase.angpos_threshold.set(old)
        waterlauncher.set_motor_velocity(0)
        watersorter.open_indoor()


    def getAction(self):
        act_without_sort =Action(
                self.shootCastlePoint,
                lambda  :self.realize_without_sort(self.wheeledbase,self.watersorter,self.waterlauncher, self.display) ,
                Shot.typ,
                "SHORTSHOOTNOSORT",
                8*Shot.POINTS_PER_BALL_CASTLE,
                Shot.TIME_UNSORTED
                )
        act_with_sort_long1 =Action(
                self.shootCastlePointLong1,
                lambda  :self.realize_with_sort(self.wheeledbase,self.watersorter,self.waterlauncher, self.display) ,
                Shot.typ,
                "LONGSHOOTSORT1",
                4 * Shot.POINTS_PER_BALL_CASTLE,
                Shot.TIME_SORTED
                )
        def launch_motor():
            self.waterlauncher.set_motor_pulsewidth(1100)
            time.sleep(0.1)
            self.watersorter.enable_shaker_equal()
            print("MOTOR LAUNCHING")
        act_without_sort.set_before_action(launch_motor)
        act_with_sort_long1.set_before_action(launch_motor)
        return [act_without_sort,act_with_sort_long1]


class Treatment(Actionnable):
    typ="treatement"
    POINTS = 40
    TIME = 10
    POINTS_PER_BALL = 10
    def __init__(self, side, rm, geo, arduinos, display, mover, logger, data):
        self.side=side
        self.rm=rm
        self.mover = mover
        self.geo = geo
        self.logger = logger
        self.display = display
        self.wheeledbase = arduinos["wheeledbase"]
        self.watersorter = arduinos["watersorter"]
        self.shootTreatmentPoint=self.geo.get('ShootTreatment'+str(self.side))
        self.treatmentPoint=self.geo.get('Treatment'+str(self.side))
        self.data = data
        
    def realize(self,robot,waterSorter):
        self.logger("TREATMENT :", "Go to the drop point !")
        currentPosXY=robot.get_position()[:2]
        try:
            self.mover.turnonthespot(math.pi, 3, stategy=Mover.AIM)
        except PositionUnreachable:
            return

        self.display.angry(1)
        self.logger("TREATMENT :", "Launch a go wall ")
        try:
            self.mover.gowall(3,direction="backward", strategy=Mover.POSITION, position=self.shootTreatmentPoint)
        except PositionUnreachable:
            self.logger("TREATMENT :", "Position Unreachable ")
            pass
        turn = False
        self.logger("TREATMENT :", "Turning !")
        try:
            self.wheeledbase.goto_delta(70, 0)
            self.wheeledbase.wait()
            self.mover.turnonthespot(math.pi / 2, 3, stategy=Mover.AIM)

        except RuntimeError:
            try:
                self.mover.turnonthespot(math.pi / 2, 3, stategy=Mover.AIM)
            except PositionUnreachable:
                return

        self.display.happy(2)
        self.logger("TREATMENT :", "Droping !")
        waterSorter.open_trash_unloader()
        time.sleep(2)
        self.display.addPoints(self.data["nb_balls_in_unloader"]*Treatment.POINTS_PER_BALL)
        waterSorter.open_trash()
        time.sleep(0.7)
        waterSorter.close_trash()
        time.sleep(2)
        waterSorter.close_trash_unloader()
        
        self.mover.turnonthespot(0, -1, stategy=Mover.AIM)
        self.mover.withdraw(*currentPosXY, direction="backward")

    def all_in_treatment(self):
        

    #override
    def getAction(self):
        act =Action(
                self.treatmentPoint,
                lambda  :self.realize(self.wheeledbase ,self.watersorter) ,
                Treatment.typ,
                "TREATMENT",
                Treatment.POINTS,
                Treatment.TIME
            )
        return [act]

