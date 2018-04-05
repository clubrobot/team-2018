from geogebra import GeoGebra

import math
import time
from automateTools import AutomateTools
from action import *
#Ouverture du ficher
geo = GeoGebra('bornibus.ggb')

class Dispenser(Actionnable):
    typ="Dispenser"
    def __init__(self,numberDispenser, rm, wheeledbase, watersorter):
        self.rm=rm
        self.numberDispenser=numberDispenser
        self.watersorter = watersorter
        self.wheeledbase = wheeledbase
        self.targetPoint=geo.get('Dispenser'+str(self.numberDispenser)+'_1')
        self.preparationPoint=geo.get('Dispenser'+str(self.numberDispenser)+'_0')

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
            self.watersorter.disable_shaker()
        init_pos = robot.get_position()[:-1]

        robot.set_velocities(-200,0)
        pos = robot.get_position()[:-1]
        while math.hypot(pos[0]-init_pos[0],pos[1]-init_pos[1])<300:
            time.sleep(0.5)
            pos = robot.get_position()[:-1]
        
        robot.stop()

    def funForWaitDisp(self,robot,path):
        if True:
            robot.purepursuit(path)
        else :
            return AutomateTools.stopThisAction
        
    def getAction(self):
        return [Action(self.preparationPoint,lambda : self.realize(self.wheeledbase,self.watersorter ),Dispenser.typ)]





class ShootGestion():
    fullA="fullA"
    fullB="fullB"
    alternateA="alternateA"
    alternateB="alternateB"

    sideOfDispenser = {
        1 : fullB,
        2 : alternateA,
        3 : alternateB,
        4 : fullA
    }
    
    emptyTyp="emptyTyp"

    numberTotalBalls=8#not used

    @staticmethod
    def getIfTheActionYouHaveToShotOrToTreat(side,robot,id):
        #First boolis for Shot (you have to shot something), 
        #second bool is for treatment(you have to treat something)
        whatActionHaveIToDo = {
            'A' : {
                ShootGestion.fullA : (True,False),
                ShootGestion.alternateB : (True,True), 
                ShootGestion.alternateA : (True,True),
                ShootGestion.fullB : (False,True)
            },
            'B' : {
                 ShootGestion.fullA : (False,True),
                ShootGestion.alternateB : (True,True),
                ShootGestion.alternateA : (True,True),
                ShootGestion.fullB : (True,False)
            }
        }
        listShotCall = whatActionHaveIToDo[side][ShootGestion.sideOfDispenser[id]]
        return listShotCall

class Shot(Actionnable):
    typ="shot"
    def __init__(self,side,rm,wheeledbase,watersorter,waterlauncher):
        self.side=side
        self.rm=rm
        self.wheeledbase = wheeledbase
        self.watersorter = watersorter
        self.waterlauncher = waterlauncher
        self.shootCastlePoint=geo.get('ShootCastle'+str(self.side))
        self.castlePoint=geo.get('Castle'+str(self.side))
        
        
    def realize_without_sort(self,wheeledbase, watersorter, waterlauncher,global_timeout=30):
        currentPosXY=wheeledbase.get_position()[:2]
        theta = math.atan2(self.castlePoint[1]-currentPosXY[1],self.castlePoint[0]-currentPosXY[0])
        wheeledbase.turnonthespot(theta)
        old = wheeledbase.angpos_threshold.get()
        wheeledbase.angpos_threshold.set(0.1)
       
        time.sleep(0.2)
        watersorter.enable_shaker()
        watersorter.write_trash(126)
        watersorter.open_indoor()
        #watersorter.close_outdoor()
        nb_balls = 0
        watersorter.open_outdoor()
        begin = time.time()
        accu = 0
        motor_base = 75
        waterlauncher.set_motor_pulsewidth(1000+motor_base)
        time.sleep(4) # Wait the motor running 
        new_ball = 1
        last_time = begin - 10
        while nb_balls < 8 and time.time() - begin < global_timeout:
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
        time.sleep(3)

#        while nb_balls<8:
#            print("Salve")
#            open_time = time.time()
#            watersorter.open_indoor()
#            while not (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100 or time.time() - open_time > timeout):
#                time.sleep(0.05)
#            print("Balle 1")
#
#            open_time = time.time()
#            while not (watersorter.get_water_color()[0]<100 or watersorter.get_water_color()[1]<100 or time.time() - open_time > timeout):
#                time.sleep(0.05)
#
#            time.sleep(0.3)
#            watersorter.close_indoor()
#            open_time = time.time()
#            while not (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100 or time.time() - open_time > timeout):
#                time.sleep(0.05)
#            print("Balle 2")
#
#            
#            while (time.time() - open_time < 3):
#                time.sleep(0.1)
#            
#            nb_balls +=2

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
        motor_base = 75
        waterlauncher.set_motor_pulsewidth(1000+motor_base)
        time.sleep(4) # Wait the motor running
        watersorter.enable_shaker()
        watersorter.write_trash(128)
        watersorter.close_indoor()
        watersorter.write_trash_unloader(100)
        watersorter.close_outdoor()
        timeout_reached = False
        nb_ball = 0
        while not timeout_reached and nb_ball<8:
            watersorter.open_indoor()
            watersorter.close_trash()
            watersorter.close_outdoor()
            open_time = time.time()
            while time.time()-open_time<timeout and not (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100):
                time.sleep(0.3)
                print(watersorter.get_water_color())
            if time.time()-open_time>(timeout):
                print("TIMEOUT")
            #Verification de la sortie dans le canon

            time.sleep(0.7)
            nb_ball+=1
            print("New ball geted ! {}".format(nb_ball))
            # On verifie si la code couleur est bon
            if(watersorter.get_water_color()[0]<watersorter.get_water_color()[1]):
                watersorter.open_outdoor()
            else:
                watersorter.open_trash()

            while (watersorter.get_water_color()[0]>100 or watersorter.get_water_color()[1]>100):
                time.sleep(0.4)
                print("En attente de la sortie")
            time.sleep(1.3)
        watersorter.disable_shaker()
        wheeledbase.angpos_threshold.set(old)
        waterlauncher.set_motor_velocity(0)


    def getAction(self):
        
        act_without_sort =Action(
                self.shootCastlePoint,
                lambda  :self.realize_without_sort(self.wheeledbase,self.watersorter,self.waterlauncher) ,
                Shot.typ
                )
        act_with_sort =Action(
                self.shootCastlePoint,
                lambda  :self.realize_with_sort(self.wheeledbase,self.watersorter,self.waterlauncher) ,
                Shot.typ
                )   
        return [act_without_sort,act_with_sort]


class Treatment(Actionnable):
    typ="treatement"
    def __init__(self,side,rm,wheeledbase,watersorter):
        self.side=side
        self.rm=rm
        self.wheeledbase = wheeledbase
        self.watersorter = watersorter
        self.shootTreatmentPoint=geo.get('ShootTreatment'+str(self.side))
        self.treatmentPoint=geo.get('Treatment'+str(self.side))
        
    def realize(self, shotDirection,robot,waterSorter):
        currentPosXY=robot.get_position()[:2]
        robot.purepursuit([currentPosXY,shotDirection])
        
        robot.wait()
        robot.turnonthespot(3.141592/2)
        robot.wait()
        waterSorter.open_trash_unloader()
        time.sleep(2)
        waterSorter.open_trash()
        time.sleep(0.7)
        waterSorter.close_trash()
        time.sleep(2)
        waterSorter.close_trash_unloader()
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
from geogebra import GeoGebra

import math
import time
