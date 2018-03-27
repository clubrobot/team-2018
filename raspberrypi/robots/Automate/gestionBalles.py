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
        theta = math.atan2(self.preparationPoint[1]-self.targetPoint[1],self.preparationPoint[0]-self.targetPoint[0])

        robot.turnonthespot(theta)
        robot.wait()
        path = [self.preparationPoint,self.targetPoint]
        robot.purepursuit(path,direction='backward')

        #AutomateTools.myPurepursuite(robot,path)
        #AutomateTools.myTurnonthespot(robot,robot.get_position()[-1] +3.141592)

        try:
            robot.wait()
        except RuntimeError:
            self.watersorter.enable_shaker()
            time.sleep(3)
            self.watersorter.disable_shaker()


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
        
        
    def realize(self,wheeledbase, watersorter, waterlauncher):
        currentPosXY=wheeledbase.get_position()[:2]
        theta = math.atan2(self.castlePoint[1]-currentPosXY[1],self.castlePoint[0]-currentPosXY[0])
        wheeledbase.turnonthespot(theta)
        old = wheeledbase.angpos_threshold.get()
        wheeledbase.angpos_threshold.set(0.1)
        time.sleep(0.2)
        waterlauncher.set_motor_velocity(13)#9
        watersorter.enable_shaker()
        watersorter.write_trash(129)
        watersorter.close_indoor()
        watersorter.close_outdoor()
        time.sleep(0.3)
        for i in range(6):
            watersorter.open_indoor()
            watersorter.close_outdoor()
            time.sleep(1.3)
            watersorter.close_indoor()
            watersorter.open_outdoor()
            time.sleep(1.3)
        watersorter.disable_shaker()
        wheeledbase.angpos_threshold.set(old)
        waterlauncher.set_motor_velocity(0)
            

    #override
    def getAction(self):
        
        act =Action(
                self.shootCastlePoint,
                lambda  :self.realize(self.wheeledbase,self.watersorter,self.waterlauncher) ,
                Shot.typ
                )
        return [act]


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
        theta = math.atan2(shotDirection[1]-currentPosXY[1],shotDirection[0]-currentPosXY[0])
        AutomateTools.myTurnonthespot(robot,theta)
        #AutomateTools.myDrop(waterSorter)

    #override
    def getAction(self):
        act =Action(
                self.shootTreatmentPoint,
                lambda  :self.realize(self.treatmentPoint,self.wheeledbase ,self.watersorter) ,
                Treatment.typ
            )
        return [act]