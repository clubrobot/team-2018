from geogebra import GeoGebra

import math
import time
from automateTools import AutomateTools
from action import *



class Interrupteur(Actionnable):
    typ="Interrupteur"
    POINTS = 25
    def __init__(self,side, geo, wheeledbase, display, mover):
        self.side=side
        self.mover = mover
        self.wheeledbase = wheeledbase
        self.display = display
        self.preparation=geo.get('Interrupteur'+str(self.side)+'_0')
        self.interrupteur=geo.get('Interrupteur'+str(self.side)+'_1')

    def realize(self,robot, display):
        #print("Realisation")
        theta = math.atan2(self.interrupteur[1]-self.preparation[1],self.interrupteur[0]-self.preparation[0])
        AutomateTools.myTurnonthespot(robot,theta)
        path = [ self.preparation, self.interrupteur]
        robot.purepursuit(path)
            #si on patine alors on stop l'action
        AutomateTools.myWait(robot,lambda : AutomateTools.stopThisAction)
        robot.goto(self.preparation[0],self.preparation[1])
        try:
            robot.wait()
        except:
            pass
        display.addPoints(Interrupteur.POINTS)

        #override Actionnable
    def getAction(self):
            return [Action(self.preparation,lambda : self.realize(self.wheeledbase, self.display),Interrupteur.typ) ]

class Abeille(Actionnable):
    typ="Abeille"
    POINTS = 50
    def __init__(self, side, geo, wheeledbase, display, beeActioner,mover):
        self.side=side
        self.mover = mover
        self.wheeledbase = wheeledbase
        self.display = display
        self.beeActioner = beeActioner
        self.preparation=geo.get('Abeille'+str(self.side)+'_0')
        self.interrupteur=geo.get('Abeille'+str(self.side)+'_1')

    def realize(self,robot, display):
        self.beeActioner.open()
        robot.turnonthespot(math.pi)
        robot.wait()
        robot.purepursuit([self.preparation, self.interrupteur], direction="backward")
        robot.wait()
        robot.turnonthespot(math.pi+(self.side*2-1)*math.pi/8)
        robot.wait()
        robot.set_velocities(0, -(self.side*2-1)*9)
        time.sleep(0.5)
        robot.goto(*self.preparation)
        robot.wait()
        self.beeActioner.close()
        display.addPoints(Abeille.POINTS)

        #override Actionnable
    def getAction(self):
            return [Action(self.preparation,lambda : self.realize(self.wheeledbase, self.display),Interrupteur.typ) ]

class Odometrie(Actionnable):
    typ="Odometrie"
    def __init__(self, side, geo,id):#id = 0 (vers le bas) ou 1(vers la droite)
        self.side=side
        self.preparation=geo.get('Odometrie'+str(self.side)+'_{'+str(id)+'}')
        self.mur=geo.get('Odometrie'+str(self.side)+'_{'+str(id)+',0}')

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