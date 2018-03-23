from geogebra import GeoGebra

import math
from automateTools import AutomateTools
from action import *
#Ouverture du ficher
geo = GeoGebra('murray.ggb')


class Depot(Actionnable):
    typ="Depot"
    def __init__(self,side,numberDepot,rm):
        self.rm=rm
        #side must be A or B 
        assert(side == 'A' or side=='B')
        #point d'orientation
        self.point0=geo.get('Depot'+side+'_{'+str(numberDepot)+'0}')
        #point de dépot
        self.point1=geo.get('Depot'+side+'_{'+str(numberDepot)+'1}')

    def realize(self,robot,builderCollector) : 
        theta = math.atan2(self.point0[1]-self.point1[1],self.point0[0]-self.point1[0])
        AutomateTools.myTurnonthespot(robot,theta)
        AutomateTools.myPurepursuite(robot,(robot.get_position()[:2],self.point1),direction="backward")
        builderCollector.drop_tower()
        AutomateTools.myWait(robot,lambda : builderCollector.drop_tower())

    def getAction(self,robot,builerCollector,waterDispenser):
        return [Action(self.point0,lambda : self.realize(robot,builerCollector),Depot.typ) ]

    def __str__(self):
        return "DEPOT OBJ"
    def __repr__(self):
        return str(self)

class CubesSpotPoints(Actionnable):
    cutlines=[]
    typ="CubesSpotPoints"

    #schema des access :
    #          2
    #          ⬜
    #       0⬜⬜⬜3
    #          ⬜
    #          1
    def __init__(self,numberCroix,rm):
        self.rm=rm
        self.numberCroix=numberCroix
        self.access=[]
        for i in range(4):
            self.access.append(self.doAcessInTheRightOrder(i))
        initCutlinesNumber = len(geo.getall('Croix'+str(numberCroix)+'_{intersection.*}'))//2
        self.cutlinesInit=[]
        for i in range(initCutlinesNumber):
            self.cutlinesInit.append(geo.getall('Croix'+str(numberCroix)+'_{intersection'+str(i)+'.*}'))

        for cut in self.cutlinesInit:
            rm.cut_edges(cut)
            CubesSpotPoints.cutlines.append(cut)
    #utilisé pour l'initialisation
    def doAcessInTheRightOrder(self,id):
        accessDetails=[]
        for i in range(4):
            accessDetails.append(geo.get('Croix'+str(self.numberCroix)+'_{'+str(id)+str(i)+'}'))
        return accessDetails

    #coupe les edges qui sont encore néssessaires (ceux de la variable de classe cutlines)
    def cutEdgesNecessary(self):
        for cutline in CubesSpotPoints.cutlines:
            self.rm.cut_edges(cutline)
    
    #prise des cubes
    def realize(self,major,robot,builderCollector):
        #print("access "+str(major if major<4 else 0 ))
        c1,c2,c3,c4=self.access[major if major<4 else 0]
        theta = math.atan2(c2[1]-c1[1],c2[0]-c1[0])
        AutomateTools.myTurnonthespot(robot,theta)

        AutomateTools.myGrab(robot,lambda : builderCollector.grab_center(),(c1,c2))#Fait path c1,c2 PUIS grab
        AutomateTools.myGrab(robot,lambda : builderCollector.grab_right(),(c2,c3))
        AutomateTools.myGrab(robot,lambda : builderCollector.grab_left())
        AutomateTools.myGrab(robot,lambda : builderCollector.grab_center())
        AutomateTools.myGrab(robot,lambda : builderCollector.grab_center(),(c3,c4))
        self.updateRoadMap()#retire les cubes de la map (cutlines)

    #override Actionnable
    def getAction(self,robot,builderCollector,waterDispenser):
        act= [Action(self.access[majo][0],lambda maj=majo: self.realize(maj,robot,builderCollector),CubesSpotPoints.typ) for majo in range(len(self.access)) ]
        return act
    #lorsque que la prise est terminée, on remet les edges liés à ce dépot
    def updateRoadMap(self):
        for cut in self.cutlinesInit:
            CubesSpotPoints.cutlines.remove(cut)
        self.rm.reset_edges()#restore all
        self.cutEdgesNecessary()#remove again the unecessary

#gere tous les dépots disponibles
class DepotGestion:
    
    def __init__(self,side,rm):
        self.depotsDone= []
        self.depots = [Depot(side,X,rm) for X in range(len(geo.getall('Depot'+side+'_{.*}'))//2)]
    
    def getDepotAvaible(self):
        return [depot for depot in self.depots if depot not in self.depotsDone]
   
    #rajoute le depot à la liste des dépots fait
    def done(self,depot):
        self.depotsDone.append(depot)

    def realize(self,robot,builder):
        self.realizeFirstDepotAvaible(robot,builder)
    
    #donne le 1er dépot dispo
    #de l'exterieur vers l'intérieur du terrain
    def getFirstDepotAvaibleAndDoneIt(self):
        avaibles=self.getDepotAvaible()
        if len(avaibles)==0:
            print("no depots avaibles")
        else:          
            #-1 for the last one (closer than start point, to evite collision with other towers)
            self.done(avaibles[-1])
            return avaibles[-1]

    #REALIZE le 1er dépot dispo
    #de l'exterieur vers l'intérieur du terrain
    def realizeFirstDepotAvaible(self,robot,builder):
        avaibles=self.getDepotAvaible()
        if len(avaibles)==0:
            print("no depots avaibles")
        else:          
            #-1 for the last one (closer than start point, to evite collision with other towers)
            (avaibles[-1]).goDeposer(robot,builder)
            self.done(avaibles[-1])