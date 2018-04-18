#!/usr/bin/env python3
# coding: utf-8

import math
import time

from robots.automateTools import AutomateTools
from robots.action import Action, Actionnable


class Dispenser(Actionnable):
    typ="Dispenser"
    POINTS_DISPENSER = 10
    def __init__(self,numberDispenser, rm, geo, arduinos, display, mover):
        self.rm  = rm
        self.geo = geo
        self.mover = mover
        self.display = display
        self.numberDispenser=numberDispenser
        self.watersorter = arduinos["watersorter"]
        self.wheeledbase = arduinos["wheeledbase"]
        self.targetPoint=self.geo.get('Dispenser'+str(self.numberDispenser)+'_1')
        self.preparationPoint=self.geo.get('Dispenser'+str(self.numberDispenser)+'_0')

    def realize(self,robot ,watersorter ,display):
        theta = math.atan2(self.preparationPoint[1]-self.targetPoint[1],self.preparationPoint[0]-self.targetPoint[0])+3.141592
        robot.max_linvel.set(300)
        robot.max_angvel.set(1)
        watersorter.close_trash()
        watersorter.close_outdoor()
        watersorter.open_indoor()
        robot.turnonthespot(theta)
        while True:
            try:
                robot.wait()
                break
            except:
                time.sleep(0.2)
                robot.turnonthespot(theta)

        path = [self.preparationPoint,self.targetPoint]
        robot.purepursuit(path,direction='forward')
        robot.max_linvel.set(500)
        robot.max_angvel.set(6)
        display.addPoints(Dispenser.POINTS_DISPENSER)
        #AutomateTools.myPurepursuite(robot,path)
        #AutomateTools.myTurnonthespot(robot,robot.get_position()[-1] +3.141592)

        try:
            robot.wait()
        except RuntimeError:
            self.watersorter.enable_shaker()
            time.sleep(3)
            
        init_pos = robot.get_position()[:-1]

        robot.set_velocities(-200,0)
        pos = robot.get_position()[:-1]
        while math.hypot(pos[0]-init_pos[0],pos[1]-init_pos[1])<250:
            try:
                robot.isarrived()
                time.sleep(0.2)
            except RuntimeError:
                robot.stop()
                robot.set_velocities(100,0)
                time.sleep(1)
                robot.stop()
                time.sleep(0.2)
                robot.purepursuit([pos,self.preparationPoint], direction="backward")
                time.sleep(0.2)
                
            time.sleep(0.5)
            pos = robot.get_position()[:-1]

        self.watersorter.disable_shaker()
        robot.stop()
        
        

    def funForWaitDisp(self,robot,path):
        if True:
            robot.purepursuit(path)
        else :
            return AutomateTools.stopThisAction
        
    def getAction(self):
        return [Action( self.preparationPoint,
                        lambda : self.realize(self.wheeledbase,self.watersorter, self.display),
                        Dispenser.typ, 
                        "DISPENSER"+str(self.numberDispenser))]


class Shot(Actionnable):
    typ="shot"
    POINTS_PER_BALL_CASTLE = 5
    POINTS_PER_BALL_EPURATION = 10
    def __init__(self, side, rm, geo, arduinos, display, mover):
        self.side=side
        self.rm  = rm
        self.geo = geo
        self.mover  = mover
        self.wheeledbase = arduinos["wheeledbase"]
        self.watersorter = arduinos["watersorter"]
        self.waterlauncher = arduinos["waterlauncher"]
        self.display = display
        self.shootCastlePoint=self.geo.get('ShootCastle'+str(self.side))
        self.shootCastlePointLong=self.geo.get('ShootCastleLong'+str(self.side))
        self.castlePoint=self.geo.get('Castle'+str(self.side))
        
        
    def realize_without_sort(self, wheeledbase, watersorter, waterlauncher, display, global_timeout=20):
        currentPosXY=wheeledbase.get_position()[:2]
        theta = math.atan2(self.castlePoint[1]-currentPosXY[1],self.castlePoint[0]-currentPosXY[0])
        wheeledbase.turnonthespot(theta)
        old = wheeledbase.angpos_threshold.get()
        wheeledbase.angpos_threshold.set(0.1)
        watersorter.enable_shaker()
        watersorter.close_trash()
        watersorter.open_indoor()
        watersorter.close_outdoor()
        nb_balls = 0
        begin_time = time.time()
        accu = 0
        motor_base = 76
        waterlauncher.set_motor_pulsewidth(1000+motor_base)
        time.sleep(3)# Wait the motor running 
        watersorter.open_outdoor()
        new_ball = 1
        last_time = begin_time - 10
        timeout_per_ball = 1
        points = 0
        while nb_balls < 8 and time.time() - begin_time < global_timeout:
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            watersorter.open_indoor()
            watersorter.close_outdoor()
            open_time = time.time()
            while not (time.time() - begin_time > global_timeout) and not (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100):
                time.sleep(0.2)
                if time.time() - open_time > timeout_per_ball:
                    watersorter.close_trash()
                    open_time = time.time()
            
            time.sleep(0.3)
            
            watersorter.close_indoor()
            watersorter.open_outdoor()

            close_time = time.time()
            while (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100) and not (time.time() - begin_time > global_timeout):
                time.sleep(0.2)

                waterlauncher.set_motor_pulsewidth(1000+motor_base)
                if time.time() - close_time > timeout_per_ball:
                    watersorter.close_trash()
                    close_time = time.time()
            
            time.sleep(0.5)
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            if time.time() - begin_time < global_timeout:
                nb_balls +=1
                display.addPoints(Shot.POINTS_PER_BALL_CASTLE)
            #
            #print(time.time() - begin)
            #if(watersorter.get_water_color()[0]>120 or watersorter.get_water_color()[1]>120) and new_ball:
            #    new_ball = 0
            #    nb_balls += 1
            #    print("+1 balle")
            #    display.addPoints(Shot.POINTS_PER_BALL_CASTLE)
            #
            #else:
            #    if(new_ball == 0):
            #        accu += 6/(time.time() - last_time)
            #        print("Speed += ", 6/(time.time() - last_time))
            #    last_time = time.time()
            #    new_ball =1
            #
            #if time.time() - last_time > timeout_per_ball:
            #    watersorter.close_trash()
            #    last_time = time.time()
                
#
#            time.sleep(0.05)
#            accu = max(accu -6, 0)
#            speed = int(motor_base+accu)
#            speed = max(speed, motor_base)
#            speed = min(speed, motor_base+25)
#            waterlauncher.set_motor_pulsewidth(1000+speed)
#            #waterlauncher.set_motor_velocity(speed)
#            print("accu : ", accu, "    speed : ", speed)
        time.sleep(1)# Ancien 3


        watersorter.disable_shaker()
        wheeledbase.angpos_threshold.set(old)
        waterlauncher.set_motor_velocity(0)
        watersorter.close_outdoor()
        watersorter.open_indoor()
            
    def realize_with_sort(self,wheeledbase, watersorter, waterlauncher, display, timeout=5):
        currentPosXY=wheeledbase.get_position()[:2]
        theta = math.atan2(self.castlePoint[1]-currentPosXY[1],self.castlePoint[0]-currentPosXY[0])
        wheeledbase.turnonthespot(theta)
        old = wheeledbase.angpos_threshold.get()
        wheeledbase.angpos_threshold.set(0.1)
       
        time.sleep(0.2) 
        motor_base = 102
        waterlauncher.set_motor_pulsewidth(1000+motor_base)
        time.sleep(2) # Wait the motor running
        watersorter.enable_shaker()
        watersorter.close_indoor()
        watersorter.write_trash_unloader(100)
        watersorter.close_outdoor()
        nb_ball = 0
        global_timeout = 14
        begin_time = time.time()
        while not (time.time() - begin_time > global_timeout) and nb_ball<8:
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            watersorter.open_indoor()
            watersorter.close_trash()
            watersorter.close_outdoor()
            open_time = time.time()

            while not (time.time() - begin_time > global_timeout) and not (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100):
                time.sleep(0.2)
                #print(watersorter.get_water_color())

            time.sleep(0.3)
            #Verification de la sortie dans le canon
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            watersorter.close_indoor()
            nb_ball+=1
            print("New ball gotten ! {}".format(nb_ball))
            # On verifie si la code couleur est bon
            #TODO faire un timeout
            if(watersorter.get_water_color()[0]<watersorter.get_water_color()[1]) and not (time.time() - begin_time > global_timeout):
                if self.side==0:
                    watersorter.open_outdoor()
                    display.addPoints(Shot.POINTS_PER_BALL_CASTLE)
                else:
                    watersorter.open_trash()
                    display.addPoints(Shot.POINTS_PER_BALL_EPURATION)
            else:
                if self.side==0:
                    watersorter.open_trash()
                else:
                    watersorter.open_outdoor()

            while (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100) and not (time.time() - begin_time > global_timeout):
                time.sleep(0.1)
                print("En attente de la sortie")
                waterlauncher.set_motor_pulsewidth(1000+motor_base)

            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            time.sleep(0.3)
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
                "SHORTSHOOTNOSORT"
                )
        act_with_sort =Action(
                self.shootCastlePoint, #self.shootCastlePointLong,
                lambda  :self.realize_with_sort(self.wheeledbase,self.watersorter,self.waterlauncher, self.display) ,
                Shot.typ,
                "SHORTSHOOTSORT"
                )
        act_with_sort_long =Action(
                self.shootCastlePointLong,
                lambda  :self.realize_with_sort(self.wheeledbase,self.watersorter,self.waterlauncher, self.display) ,
                Shot.typ,
                "LONGSHOOTSORT"
                )   
        return [act_without_sort,act_with_sort,act_with_sort_long]


class Treatment(Actionnable):
    typ="treatement"
    def __init__(self, side, rm, geo, arduinos, mover):
        self.side=side
        self.rm=rm
        self.mover = mover
        self.geo = geo
        self.wheeledbase = arduinos["wheeledbase"]
        self.watersorter = arduinos["watersorter"]
        self.shootTreatmentPoint=self.geo.get('ShootTreatment'+str(self.side))
        self.treatmentPoint=self.geo.get('Treatment'+str(self.side))
        
    def realize(self, shotDirection,robot,waterSorter):
        currentPosXY=robot.get_position()[:2]
        robot.purepursuit([currentPosXY,shotDirection])
        try:
            robot.wait()
        except RuntimeError:
            pass
        turn = False
        print("Turning")
        robot.turnonthespot(3.141592/2)
        while not turn:
            try:
                turn  = robot.isarrived()
            except RuntimeError:
                robot.stop()
                robot.set_velocities(-200,0)
                time.sleep(0.3)
                robot.stop()
                robot.turnonthespot(3.141592/2)

        waterSorter.open_trash_unloader()
        time.sleep(2)
        waterSorter.open_trash()
        time.sleep(0.7)
        waterSorter.close_trash()
        time.sleep(2)
        waterSorter.close_trash_unloader()
        
        robot.turnonthespot(0)
        turn = False
        while not turn:
            try:
                robot.isarrived()
                turn = True
            except RuntimeError:
                robot.set_velocities(-100,0)
                time.sleep(0.4)
                robot.stop()
                robot.turnonthespot(0)
            
        robot.goto(*currentPosXY)

    #override
    def getAction(self):
        act =Action(
                self.treatmentPoint,
                lambda  :self.realize(self.shootTreatmentPoint,self.wheeledbase ,self.watersorter) ,
                Treatment.typ,
                "TREATMENT"
            )
        return [act]

