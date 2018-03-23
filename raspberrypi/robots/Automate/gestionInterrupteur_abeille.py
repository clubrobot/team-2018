from geogebra import GeoGebra

import math
import time
from automateTools import AutomateTools
from action import *
#Ouverture du ficher
geoBornibus = GeoGebra('bornibus.ggb')


class Interrupteur(Actionnable):
    typ="Interrupteur"
    def __init__(self,side):
        self.side=side
        self.preparation=geoBornibus.get('Interrupteur'+str(self.side)+'_{0}')
        self.interrupteur=geoBornibus.get('Interrupteur'+str(self.side)+'_{1}')

    def realize(self,robot):
        #print("Realisation")
        theta = math.atan2(self.interrupteur[1]-self.preparation[1],self.interrupteur[0]-self.preparation[0])
        AutomateTools.myTurnonthespot(robot,theta)
        path = [ self.preparation, self.interrupteur]
        robot.purepursuit(path)
            #si on patine alors on stop l'action
        AutomateTools.myWait(robot,lambda : AutomateTools.stopThisAction)

        #override Actionnable
    def getAction(self,robot,builerCollector,waterDispenser):
            return [Action(self.preparation,lambda : self.realize(robot),Interrupteur.typ) ]

class Abeille(Actionnable):
    typ="Abeille"
    def __init__(self,side):
        self.side=side
        self.preparation=geoBornibus.get('Abeille'+str(self.side)+'_{0}')
        self.interrupteur=geoBornibus.get('Abeille'+str(self.side)+'_{1}')

    def realize(self,robot):
        #print("Realisation")
        theta = math.atan2(self.interrupteur[1]-self.preparation[1],self.interrupteur[0]-self.preparation[0])
        AutomateTools.myTurnonthespot(robot,theta)
        path = [ self.preparation, self.interrupteur]
        robot.purepursuit(path)
            #si on patine alors on stop l'action
        AutomateTools.myWait(robot,lambda : AutomateTools.stopThisAction)

        #override Actionnable
    def getAction(self,robot,builerCollector,waterDispenser):
            return [Action(self.preparation,lambda : self.realize(robot),Interrupteur.typ) ]

class Abeille(Actionnable):
    typ="Abeille"
    def __init__(self,side):
        self.side=side
        self.preparation=geoBornibus.get('Abeille'+str(self.side)+'_{0}')
        self.interrupteur=geoBornibus.get('Abeille'+str(self.side)+'_{1}')

    def realize(self,robot):
        #print("Realisation")
        theta = math.atan2(self.interrupteur[1]-self.preparation[1],self.interrupteur[0]-self.preparation[0])
        AutomateTools.myTurnonthespot(robot,theta)
        path = [ self.preparation, self.interrupteur]
        robot.purepursuit(path)
            #si on patine alors on stop l'action
        AutomateTools.myWait(robot,lambda : AutomateTools.stopThisAction)

        #override Actionnable
    def getAction(self,robot,builerCollector,waterDispenser):
            return [Action(self.preparation,lambda : self.realize(robot),Abeille.typ) ]

class Odometrie(Actionnable):
    typ="Odometrie"
    def __init__(self,side,id):#id = 0 (vers le bas) ou 1(vers la droite)
        self.side=side
        self.preparation=geoBornibus.get('Odometrie'+str(self.side)+'_{'+str(id)+'}')
        self.mur=geoBornibus.get('Odometrie'+str(self.side)+'_{'+str(id)+',0}')

    def realize(self,robot):
        #print("Realisation")
        theta = math.atan2(self.mur[1]-self.preparation[1],self.mur[0]-self.preparation[0])
        AutomateTools.myTurnonthespot(robot,theta)
        path = [ self.preparation, self.mur]
        robot.purepursuit(path)
            #si on patine alors on stop l'action
        AutomateTools.myWait(robot,lambda : AutomateTools.stopThisAction)

        #override Actionnable
    def getAction(self,robot,builerCollector,waterDispenser):
            return [Action(self.preparation,lambda : self.realize(robot),Odometrie.typ) ]