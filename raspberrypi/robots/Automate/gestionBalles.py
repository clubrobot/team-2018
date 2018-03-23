from geogebra import GeoGebra

import math
import time
from automateTools import AutomateTools
from action import *
#Ouverture du ficher
geo = GeoGebra('bornibus.ggb')

class Dispenser(Actionnable):
    typ="Dispenser"
    def __init__(self,numberDispenser,rm):
        self.rm=rm
        self.numberDispenser=numberDispenser
        self.targetPoint=geo.get('Dispenser'+str(self.numberDispenser)+'_{0}')
        self.preparationPoint=geo.get('Dispenser'+str(self.numberDispenser)+'_{1,action,0}')
        # for i in range(1,2):
        #     self.access.append(self.doAcessInTheRightOrder(i))
     

    # def doAcessInTheRightOrder(self,id):
    #     accessDetails=[]
    #     for i in range(1):
    #         accessDetails.append(geo.get('Dispenser'+str(self.numberDispenser)+'_{'+str(id)+',action,'+str(i)+'}'))
    #     return accessDetails


    #included in goPickUpBalls
    def realize(self,robot):
        #print("Realisation")
        
        path = [self.preparationPoint,self.targetPoint]
        # robot.purepursuit(path)
        # AutomateTools.myWait(robot,lambda : self.funForWaitDisp(robot,path))
        AutomateTools.myPurepursuite(robot,path)
        AutomateTools.myTurnonthespot(robot,robot.get_position()[-1] +3.141592)
    def funForWaitDisp(self,robot,path):
        if True:#not waterDispenser.have_ball():
            robot.purepursuit(path)
        else :
            return AutomateTools.stopThisAction
        
        #override Actionnable
    def getAction(self,robot,builerCollector,waterDispenser):
        return [Action(self.preparationPoint,lambda : self.realize(robot),Dispenser.typ)]





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
    def __init__(self,side,rm,idDispenser):
        self.side=side
        self.rm=rm
        self.idDispenser=idDispenser
        self.shootCastlePoint=geo.get('ShootCastle'+str(self.side))
        self.castlePoint=geo.get('Castle'+str(self.side))
        
        
    def realize(self, shotDirection,robot,waterLauncher):
        currentPosXY=robot.get_position()[:2]
        theta = math.atan2(shotDirection[1]-currentPosXY[1],shotDirection[0]-currentPosXY[0])
        AutomateTools.myTurnonthespot(robot,theta)
        AutomateTools.myFire(waterLauncher)

    #override
    def getAction(self,robot,waterSorter,waterLauncher):
        actAFaire = ShootGestion.getIfTheActionYouHaveToShotOrToTreat(self.side,robot,self.idDispenser) [0]#0 car correspond au shot
        if(not actAFaire): 
            currentPosXY=robot.get_position()[:2]#NOT THE GOOD POSITION (but c'est pas grave)
            act = Action(currentPosXY,lambda : (),ShootGestion.emptyTyp)
        else : 
            act =Action(
                    self.shootCastlePoint,
                    lambda  :self.realize(self.castlePoint,robot,waterLauncher) ,
                    Shot.typ
                )
        return [act]


class Treatment(Actionnable):
    typ="treatement"
    def __init__(self,side,rm,idDispenser):
        self.side=side
        self.rm=rm
        self.idDispenser=idDispenser
        self.shootTreatmentPoint=geo.get('ShootTreatment'+str(self.side))
        self.treatmentPoint=geo.get('Treatment'+str(self.side))
        
    def realize(self, shotDirection,robot,waterSorter):
        currentPosXY=robot.get_position()[:2]
        theta = math.atan2(shotDirection[1]-currentPosXY[1],shotDirection[0]-currentPosXY[0])
        AutomateTools.myTurnonthespot(robot,theta)
        AutomateTools.myDrop(waterSorter)

    #override
    def getAction(self,robot,waterSorter,waterLauncher):
        actAFaire = ShootGestion.getIfTheActionYouHaveToShotOrToTreat(self.side,robot,self.idDispenser)[1]
        if(not actAFaire): 
            currentPosXY=robot.get_position()[:2]#NOT THE GOOD POSITION (but c'est pas grave)
            act = Action(currentPosXY,lambda : (),ShootGestion.emptyTyp)
        else : 
            act =Action(
                    self.shootTreatmentPoint,
                    lambda  :self.realize(self.treatmentPoint,robot,waterSorter) ,
                    Treatment.typ
                )
        return [act]