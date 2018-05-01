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
    TIME = 10
    def __init__(self,numberDispenser, rm, geo, arduinos, display, mover, logger):
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

    def realize(self,robot ,watersorter ,display):
        theta = math.atan2(self.preparationPoint[1]-self.targetPoint[1],self.preparationPoint[0]-self.targetPoint[0])+3.141592
        robot.max_linvel.set(300)
        robot.max_angvel.set(1)
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
                self.wheeledbase.set_velocities(-150, 1)
                time.sleep(0.4)
                self.wheeledbase.set_velocities(200, -1)
                time.sleep(0.4)

        self.logger("DISPENSER : ", "Trying to go backward ")
        pos = robot.get_position()[:-1]
        self.mover.withdraw(*self.preparationPoint, direction="backward", timeout=3, strategy=Mover.HARD,
                            last_point_aim=self.preparationPoint)
        self.watersorter.disable_shaker()
        robot.stop()
        self.display.happy(2)
        self.waterlauncher.set_motor_pulsewidth(1080)
        

        
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
    def __init__(self, side, rm, geo, arduinos, display, mover, logger):
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
        self.shootCastlePointLong=self.geo.get('ShootCastleLong'+str(self.side)+'_1')
        self.castlePoint=self.geo.get('Castle'+str(self.side))
        
        
    def realize_without_sort(self, wheeledbase, watersorter, waterlauncher, display, global_timeout=23):
        currentPosXY=wheeledbase.get_position()[:2]
        theta = math.atan2(self.castlePoint[1]-currentPosXY[1],self.castlePoint[0]-currentPosXY[0])
        try:
            self.mover.turnonthespot(theta, 3, Mover.AIM)
        except PositionUnreachable:
            return
        old = wheeledbase.angpos_threshold.get()
        wheeledbase.angpos_threshold.set(0.1)
        watersorter.enable_shaker_equal()
        watersorter.close_trash()
        watersorter.open_indoor()
        watersorter.close_outdoor()
        nb_balls = 0
        begin_time = time.time()
        motor_base = 80
        watersorter.open_outdoor()
        timeout_per_ball = 1
        while nb_balls < 8 and time.time() - begin_time < global_timeout:
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            watersorter.open_indoor()
            watersorter.close_outdoor()
            open_time = time.time()

            while not (time.time() - begin_time > global_timeout) and not (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100):
                time.sleep(0.1)
                if time.time() - open_time > timeout_per_ball:
                    watersorter.close_trash()
                    open_time = time.time()
            
            time.sleep(0.2)

            watersorter.open_outdoor()
            watersorter.close_indoor()

            close_time = time.time()
            while (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100) and not (time.time() - begin_time > global_timeout):
                time.sleep(0.2)

                waterlauncher.set_motor_pulsewidth(1000+motor_base)
                if time.time() - close_time > timeout_per_ball:
                    watersorter.close_trash()
                    close_time = time.time()
            
            time.sleep(0.3)
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            if time.time() - begin_time < global_timeout:
                nb_balls += 1
                display.addPoints(Shot.POINTS_PER_BALL_CASTLE)
                display.happy(1)
            waterlauncher.set_motor_pulsewidth(1150)
            time.sleep(0.1)

        watersorter.disable_shaker()
        wheeledbase.angpos_threshold.set(old)
        waterlauncher.set_motor_velocity(0)
        watersorter.close_outdoor()
        watersorter.open_indoor()
            
    def realize_with_sort(self,wheeledbase, watersorter, waterlauncher, display, global_timeout=25):
        motor_base = 102
        waterlauncher.set_motor_pulsewidth(1000 + motor_base)
        currentPosXY=wheeledbase.get_position()[:2]
        theta = math.atan2(self.castlePoint[1]-currentPosXY[1],self.castlePoint[0]-currentPosXY[0])
        try:
            self.mover.turnonthespot(theta, 3, Mover.AIM)
        except PositionUnreachable:
            return
        old = wheeledbase.angpos_threshold.get()
        wheeledbase.angpos_threshold.set(0.1)
       
        time.sleep(1)
        watersorter.enable_shaker_equal()
        watersorter.close_indoor()
        watersorter.close_trash_unloader()
        watersorter.close_outdoor()
        nb_ball = 0
        begin_time = time.time()
        timeout_per_ball = 1
        while not (time.time() - begin_time > global_timeout) and nb_ball<8:
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            watersorter.open_indoor()
            watersorter.close_trash()
            watersorter.close_outdoor()

            close_time = time.time()
            while not (time.time() - begin_time > global_timeout) and not (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100):
                time.sleep(0.1)
                #print(watersorter.get_water_color())
                if time.time() - close_time > timeout_per_ball:
                    watersorter.close_trash()
                    close_time = time.time()


            time.sleep(0.3)
            #Verification de la sortie dans le canon
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            watersorter.close_indoor()
            nb_ball+=1
            # On verifie si la code couleur est bon
            #TODO faire un timeout
            if(watersorter.get_water_color()[0]<watersorter.get_water_color()[1]) and not (time.time() - begin_time > global_timeout):
                if self.side==0:
                    watersorter.open_outdoor()
                    display.addPoints(Shot.POINTS_PER_BALL_CASTLE)
                    display.happy(1)
                else:
                    watersorter.open_trash()
                    display.addPoints(Shot.POINTS_PER_BALL_EPURATION)
                    display.sleep(1)
            else:
                if self.side==1:
                    watersorter.open_trash()
                    display.addPoints(Shot.POINTS_PER_BALL_EPURATION)
                    display.sleep(1)
                else:
                    watersorter.open_outdoor()
                    display.addPoints(Shot.POINTS_PER_BALL_CASTLE)
                    display.happy(1)

            while (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100) and not (time.time() - begin_time > global_timeout):
                time.sleep(0.1)
                self.logger("SHOT : ", "En attente de la sortie")
                waterlauncher.set_motor_pulsewidth(1000+motor_base)

            waterlauncher.set_motor_pulsewidth(1150)
            time.sleep(0.1)
            waterlauncher.set_motor_pulsewidth(1000 + motor_base)

        time.sleep(1)
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
        act_with_sort =Action(
                self.shootCastlePoint, #self.shootCastlePointLong,
                lambda  :self.realize_with_sort(self.wheeledbase,self.watersorter,self.waterlauncher, self.display) ,
                Shot.typ,
                "SHORTSHOOTSORT",
                4 * Shot.POINTS_PER_BALL_CASTLE,
                Shot.TIME_SORTED
                )
        act_with_sort_long =Action(
                self.shootCastlePointLong,
                lambda  :self.realize_with_sort(self.wheeledbase,self.watersorter,self.waterlauncher, self.display) ,
                Shot.typ,
                "LONGSHOOTSORT",
                4 * Shot.POINTS_PER_BALL_CASTLE,
                Shot.TIME_SORTED
                )
        def launch_motor():
            self.waterlauncher.set_motor_pulsewidth(1100)
            time.sleep(0.2)
            print("MOTOR LAUNCHING")
        act_without_sort.set_before_action(launch_motor)
        act_with_sort.set_before_action(launch_motor)
        act_with_sort_long.set_before_action(launch_motor)
        return [act_without_sort,act_with_sort,act_with_sort_long]


class Treatment(Actionnable):
    typ="treatement"
    POINTS = 40
    TIME = 10
    def __init__(self, side, rm, geo, arduinos, display, mover, logger):
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
        
    def realize(self, shotDirection,robot,waterSorter):
        self.logger("TREATMENT :", "Go to the drop point !")
        currentPosXY=robot.get_position()[:2]
        self.display.angry(1)
        try:
            self.mover.gowall(1)
        except PositionUnreachable:
            pass
        turn = False
        self.logger("TREATMENT :", "Turning !")
        try:
            self.mover.turnonthespot(math.pi/2, 3, stategy=Mover.AIM)
        except PositionUnreachable:
            return

        self.display.happy(2)
        self.logger("TREATMENT :", "Droping !")
        waterSorter.open_trash_unloader()
        time.sleep(2)
        waterSorter.open_trash()
        time.sleep(0.7)
        waterSorter.close_trash()
        time.sleep(2)
        waterSorter.close_trash_unloader()
        
        self.mover.turnonthespot(0, -1, stategy=Mover.AIM)
        try:
            robot.goto(*currentPosXY)
        except RuntimeError:
            pass

    #override
    def getAction(self):
        act =Action(
                self.treatmentPoint,
                lambda  :self.realize(self.shootTreatmentPoint,self.wheeledbase ,self.watersorter) ,
                Treatment.typ,
                "TREATMENT",
                Treatment.POINTS,
                Treatment.TIME
            )
        return [act]

