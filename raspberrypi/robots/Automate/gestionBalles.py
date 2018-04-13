from geogebra import GeoGebra

import math
import time
from automateTools import AutomateTools
from action import *

class Dispenser(Actionnable):
    typ="Dispenser"
    def __init__(self,numberDispenser, rm, geo, wheeledbase, watersorter):
        self.rm  = rm
        self.geo = geo
        self.numberDispenser=numberDispenser
        self.watersorter = watersorter
        self.wheeledbase = wheeledbase
        self.targetPoint=self.geo.get('Dispenser'+str(self.numberDispenser)+'_1')
        self.preparationPoint=self.geo.get('Dispenser'+str(self.numberDispenser)+'_0')

    def realize(self,robot,watersorter):
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
        while math.hypot(pos[0]-init_pos[0],pos[1]-init_pos[1])<300:
            try:
                robot.isarrived()
                time.sleep(0.2)
            except RuntimeError:
                robot.stop()
                robot.set_velocities(100,0)
                time.sleep(1)
                robot.stop()
                time.sleep(0.2)
                robot.set_velocities(-200,0)
                time.sleep(0.2)
                
            time.sleep(1)
            pos = robot.get_position()[:-1]
        self.watersorter.disable_shaker()
        robot.stop()

    def funForWaitDisp(self,robot,path):
        if True:
            robot.purepursuit(path)
        else :
            return AutomateTools.stopThisAction
        
    def getAction(self):
        return [Action(self.preparationPoint,lambda : self.realize(self.wheeledbase,self.watersorter ),Dispenser.typ)]


class Shot(Actionnable):
    typ="shot"
    def __init__(self, side, rm, geo, wheeledbase, watersorter, waterlauncher):
        self.side=side
        self.rm  = rm
        self.geo = geo
        self.wheeledbase = wheeledbase
        self.watersorter = watersorter
        self.waterlauncher = waterlauncher
        self.shootCastlePoint=self.geo.get('ShootCastle'+str(self.side))
        self.shootCastlePointLong=self.geo.get('ShootCastleLong'+str(self.side))
        self.castlePoint=self.geo.get('Castle'+str(self.side))
        
        
    def realize_without_sort(self,wheeledbase, watersorter, waterlauncher,global_timeout=15):
        currentPosXY=wheeledbase.get_position()[:2]
        theta = math.atan2(self.castlePoint[1]-currentPosXY[1],self.castlePoint[0]-currentPosXY[0])
        wheeledbase.turnonthespot(theta)
        old = wheeledbase.angpos_threshold.get()
        wheeledbase.angpos_threshold.set(0.1)
        print("COUCOU")
        time.sleep(0.2)
        watersorter.enable_shaker()
        watersorter.close_trash()
        watersorter.open_indoor()
        watersorter.close_outdoor()
        nb_balls = 0
        begin = time.time()
        accu = 0
        motor_base = 75
        waterlauncher.set_motor_pulsewidth(1000+motor_base)
        time.sleep(4) # Wait the motor running 
        watersorter.open_outdoor()
        new_ball = 1
        last_time = begin - 10
        while nb_balls < 8 and time.time() - begin < global_timeout:
            print(time.time() - begin)
            if(watersorter.get_water_color()[0]>120 or watersorter.get_water_color()[1]>120) and new_ball:
                new_ball = 0
                nb_balls += 1
                print("+1 balle")
            
            else:
                if(new_ball == 0):
                    accu += 8/(time.time() - last_time)
                    print("Speed += ", 8/(time.time() - last_time))
                last_time = time.time()
                new_ball =1

            time.sleep(0.05)
            accu = max(accu -6, 0)
            speed = int(motor_base+accu)
            speed = max(speed, motor_base)
            speed = min(speed, motor_base+25)
            waterlauncher.set_motor_pulsewidth(1000+speed)
            #waterlauncher.set_motor_velocity(speed)
            print("accu : ", accu, "    speed : ", speed)
        time.sleep(1)# Ancien 3


        watersorter.disable_shaker()
        wheeledbase.angpos_threshold.set(old)
        waterlauncher.set_motor_velocity(0)
        watersorter.close_outdoor()
        watersorter.open_indoor()
            
    def realize_with_sort(self,wheeledbase, watersorter, waterlauncher,timeout=5):
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
        timeout_reached = False
        nb_ball = 0
        global_timeout = 20
        begin_time = time.time()
        while not time.time() - begin_time > global_timeout and nb_ball<8:
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            watersorter.open_indoor()
            watersorter.close_trash()
            watersorter.close_outdoor()
            open_time = time.time()
            while time.time()-open_time<timeout and not (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100):
                time.sleep(0.3)
                #print(watersorter.get_water_color())

            if time.time()-open_time>timeout:
                print("TIMEOUT")
            #Verification de la sortie dans le canon
            time.sleep(0.1)
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            watersorter.close_indoor()
            time.sleep(0.4)
            nb_ball+=1
            print("New ball gotten ! {}".format(nb_ball))
            # On verifie si la code couleur est bon
            #TODO faire un timeout
            if(watersorter.get_water_color()[0]<watersorter.get_water_color()[1]):
                if self.side==0:
                    watersorter.open_outdoor()
                else:
                    watersorter.open_trash()
            else:
                if self.side==0:
                    watersorter.open_trash()
                else:
                    watersorter.open_outdoor()

            while (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100):
                time.sleep(0.3)
                print("En attente de la sortie")
                waterlauncher.set_motor_pulsewidth(1000+motor_base)
            print("at")
            waterlauncher.set_motor_pulsewidth(1000+motor_base)
            print("z")
            time.sleep(0.5)
        watersorter.disable_shaker()
        wheeledbase.angpos_threshold.set(old)
        waterlauncher.set_motor_velocity(0)
        watersorter.open_indoor()


    def getAction(self):
        act_without_sort =Action(
                self.shootCastlePoint,
                lambda  :self.realize_without_sort(self.wheeledbase,self.watersorter,self.waterlauncher) ,
                Shot.typ
                )
        act_with_sort =Action(
                self.shootCastlePoint, #self.shootCastlePointLong,
                lambda  :self.realize_with_sort(self.wheeledbase,self.watersorter,self.waterlauncher) ,
                Shot.typ
                )
        act_with_sort_long =Action(
                self.shootCastlePointLong,
                lambda  :self.realize_with_sort(self.wheeledbase,self.watersorter,self.waterlauncher) ,
                Shot.typ
                )   
        return [act_without_sort,act_with_sort,act_with_sort_long]


class Treatment(Actionnable):
    typ="treatement"
    def __init__(self, side, rm, geo, wheeledbase, watersorter):
        self.side=side
        self.rm=rm
        self.geo = geo
        self.wheeledbase = wheeledbase
        self.watersorter = watersorter
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
                Treatment.typ
            )
        return [act]

