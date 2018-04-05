#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
#sys.path.append("../Simulator/controle")
import pygame
import time
from pygame.locals import *
from setup_bornibus import *
from random import randint
from random import shuffle
from TextPrint import *
from roadmap import RoadMap

    
from gestionCubes import *
from gestionBalles import *
RAD=0.0174533


# Setup and launch the user interface

pygame.init()
fenetre = pygame.display.set_mode((150,80), RESIZABLE)
printer = TextPrint()
text="""
Automate
v0.9

"""
fenetre.fill(WHITE)
printer.reset()

[printer.print(fenetre,t) for t in text.split("\n")]
pygame.display.flip()

rm = RoadMap.load('murray.ggb')



#On peut aller cherche des choses plus précise comme :
#geo.getall('Croix2_{1.*}')


#only access 3 (right)
# impossibleAccessFor = {
#     0 : [0,1,2],
#     1 : [0,1,2],
#     2 : [1,3,0],
#     3 : [0,1,2],
#     4 : [0,1,2],
#     5 : [0,1,2]
# }

#restrain possible access
#only the access 1 (bottom)
# impossibleAccessFor = {
#     0 : [0,3,2],
#     1 : [0,3,2],
#     2 : [0,2,3],
#     3 : [0,3,2],
#     4 : [0,3,2],
#     5 : [0,3,2]
# }

#real one cubes spot
# impossibleAccessFor = {
#     0 : [2],
#     1 : [],
#     2 : [3],
#     3 : [2],
#     4 : [],
#     5 : [0]
# }

cube="cube"
dispenser = "disp"
shot = "shot"
#real one
impossibleAccessFor = {
    cube:{
        0 : [2],
        1 : [],
        2 : [3],
        3 : [2],
        4 : [],
        5 : [0]
    },
    dispenser:{
        1:[],
        2:[],
        3:[],
        4:[],
    }
}



def giveMeARandomAccessButAccessible(numberCroix):
    acc = randint(0,3)
    assert numberCroix in impossibleAccessFor
    while acc in impossibleAccessFor[cube][numberCroix]:
        acc = randint(0,3)
    return acc


def gimmeARandomStackOfActionsButPossibleAndInAConsistantOrder(robot,buildColl,watDisp,ordre,croixSpot,depots,ordreDisp,dispensers,shots):
    listelistActionsCroix = [croix.getAction(robot,buildColl,watDisp) for croix in croixSpot]
    listelistActionsDisp = [dsp.getAction(robot,buildColl,watDisp) for dsp in dispensers]
    listelistActionsShot = [sh.getAction(robot,buildColl,watDisp) for sh in shots]
    listdepots = [dep.getAction(robot,buildColl,watDisp) for dep in depots]
    DoneCubeIndex=[]
    DoneDispIndex=[]
    
    #[Act1,Act2]
    finalListActions=[]
    indexDep=0
    while len(DoneCubeIndex)+len(DoneDispIndex)!=len(listelistActionsCroix)+len(listelistActionsDisp):
        print("--------------------")
        print("select random")
        print("DoneCubeIndex : "+str(DoneCubeIndex))
        print("DoneDispIndex : "+str(DoneDispIndex))
        print("len(listelistActionsCroix) : "+str(len(listelistActionsCroix)))
        print("len(listelistActionsDisp) : "+str(len(listelistActionsDisp)))
        print("--------------------")
        
        cubeOrDisp = randint(0,1)
        if(cubeOrDisp==1 and len(DoneCubeIndex)!=len(listelistActionsCroix)):
            #on prend une série de cube
            cubeNb = randint(0,len(listelistActionsCroix)-1)
            while cubeNb in DoneCubeIndex :
                cubeNb = randint(0,len(listelistActionsCroix)-1)
                print(" random cu")

            DoneCubeIndex.append(cubeNb)
            index = ordre[cubeNb]
            acc = randint(0,len(listelistActionsCroix[cubeNb])-1)
            while acc in impossibleAccessFor[cube][index]:
                acc = randint(0,len(listelistActionsCroix[cubeNb])-1)
            print("Random CUBE ACCes "+str(acc)+" SELECTED")
            finalListActions.append(listelistActionsCroix[cubeNb][acc])
            if(indexDep>5):
                raise Exception("Erreur de dépot (generation)")
            finalListActions.append(listdepots[indexDep][0])
            indexDep+=1
        elif len(DoneDispIndex)!=len(listelistActionsDisp):
            #on prend une série de disp
            dispNb = randint(0,len(listelistActionsDisp)-1)
            while dispNb in DoneDispIndex :
                dispNb = randint(0,len(listelistActionsDisp)-1)
            DoneDispIndex.append(dispNb)

            index = ordreDisp[dispNb]
            acc = randint(0,len(listelistActionsDisp[dispNb])-1)
            while acc in impossibleAccessFor[dispenser][index]:
                acc = randint(0,len(listelistActionsDisp[dispNb])-1)
                print("random dispNBACC")

            finalListActions.append(listelistActionsDisp[dispNb][acc])
            finalListActions.append(listelistActionsShot[dispNb][0])
    finalListActions.reverse()
    return finalListActions
    

def putOnStackCubeSpot(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser):
    croi = CubesSpotPoints(index,rm)    
    logicalActionStackHardMade.append(croi.getAction(robot,builderCollector,waterDispenser)[access])
def putOnStackFirstDepot(gestionDepot,logicalActionStackHardMade,robot,builderCollector,waterDispenser):
    depo = gestionDepot.getFirstDepotAvaibleAndDoneIt()
    logicalActionStackHardMade.append(depo.getAction(robot,builderCollector,waterDispenser)[0])

def putOnStackDispAction(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser):
    d=Dispenser(index,rm)
    logicalActionStackHardMade.append(d.getAction(robot,builderCollector,waterDispenser)[access])

def putOnStackShootAction(rm,side,index,logicalActionStackHardMade,robot,builderCollector,waterDispenser):
    sh=Shot(side,rm,index)
    logicalActionStackHardMade.append(sh.getAction(robot,builderCollector,waterDispenser)[0])

def putOnStackTreatmentAction(rm,side,index,logicalActionStackHardMade,robot,builderCollector,waterDispenser):
    sh=Treatment(side,rm,index)
    logicalActionStackHardMade.append(sh.getAction(robot,builderCollector,waterDispenser)[0])

def getHarcodedStackOfAction(side,rm,robot,builderCollector,waterDispenser):
    #VERSION NON MAINTENUE
    gestionDepot=DepotGestion(side,rm)
    logicalActionStackHardMade=[]

        #schema du plateau : (dispenser)
    #       3          2    
    #                       
    #  4                    1
    #
    #       A           B

    #initilisation des dispenser et shoot

#---
    index = 1
    access=0
    putOnStackDispAction(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
    
    putOnStackShootAction(rm,side,index,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
    putOnStackTreatmentAction(rm,side,index,logicalActionStackHardMade,robot,builderCollector,waterDispenser)

#---
    index = 2
    access=0
    putOnStackDispAction(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
    
    putOnStackShootAction(rm,side,index,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
    putOnStackTreatmentAction(rm,side,index,logicalActionStackHardMade,robot,builderCollector,waterDispenser)

#---
    index = 3
    access=1
    putOnStackDispAction(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
    
    putOnStackShootAction(rm,side,index,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
    putOnStackTreatmentAction(rm,side,index,logicalActionStackHardMade,robot,builderCollector,waterDispenser)

#---
    index = 4
    access=1
    putOnStackDispAction(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
    
    putOnStackShootAction(rm,side,index,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
    putOnStackTreatmentAction(rm,side,index,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
    
#---



#     #schema du plateau : (cube)
#     #         3     0       
#     #  5                    2 
#     #      4            1        
#     #
#     #       A           B

#---
    index = 0
    access =1
    putOnStackCubeSpot(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
    
    putOnStackFirstDepot(gestionDepot,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
#---
    index = 1
    access =3
    putOnStackCubeSpot(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser)

    putOnStackFirstDepot(gestionDepot,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
#---
    index = 2
    access =0
    putOnStackCubeSpot(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser)

    putOnStackFirstDepot(gestionDepot,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
#---
    index = 3
    access =3
    putOnStackCubeSpot(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser)

    putOnStackFirstDepot(gestionDepot,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
#---
    index = 4
    access =3
    putOnStackCubeSpot(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser)

    putOnStackFirstDepot(gestionDepot,logicalActionStackHardMade,robot,builderCollector,waterDispenser)
#---
    index = 5
    access=3
    putOnStackCubeSpot(rm,index,access,logicalActionStackHardMade,robot,builderCollector,waterDispenser)

    putOnStackFirstDepot(gestionDepot,logicalActionStackHardMade,robot,builderCollector,waterDispenser)   
#---

#------------------------------------------
    logicalActionStackHardMade.reverse()
    return logicalActionStackHardMade


def runAutomate(side,robot,builderCollector,waterDispenser):
#     #A ou B (cf schema du plateau)
#     gestionDepotA=DepotGestion(side,rm)
#     gestionShootA=ShootGestion(side,rm)
#     #définition de l'ordre de sele      ction des croixx

#     #schema du plateau :
#     #         3     0       
#     #  5                    2 
#     #      4            1    
#     #
#     #       A           B


#     logicalActionStackHardMade=[]
#     #Initialisations des spots de cubes
#     #ATTENTION : obliger de tous les initialiser si on veut avoir les détours ! 
#     # sinon fait comme si les blocs n'existent pas
#     ordre=[0,1,2,3,4,5]    
#     #shuffle(ordre) 
#     croix=[]
#     depots=[]
#     for spot in ordre:
#         croi = CubesSpotPoints(spot,rm)
#         croix.append(croi)
#         depo = gestionDepotA.getFirstDepotAvaibleAndDoneIt()
#         depots.append(depo)
#         logicalActionStackHardMade.append(croi.getAction(robot,builderCollector,waterDispenser)[0])
#         logicalActionStackHardMade.append(depo.getAction(robot,builderCollector,waterDispenser)[0])
        
#     #initilisation des dispenser et shoot
#     ordreD=[1,2,3,4]
#     #shuffle(ordreD)
#     dispensers=[]
#     shoots = []
#     for i in ordreD:
#         d=Dispenser(i,rm)
#         dispensers.append(d)
#         sh=Shot(side,rm,i)
#         shoots.append(sh)
#         logicalActionStackHardMade.append(d.getAction(robot,builderCollector,waterDispenser)[0])
#         logicalActionStackHardMade.append(sh.getAction(robot,builderCollector,waterDispenser)[0])


#     all = croix+dispensers+shoots
#     allActions=[]
#     for act in all:
#         allActions.append(act.getAction(robot,builderCollector,waterDispenser))


    
#     #realisations des actions de récup de cubes et dépot
#     # for croi in croix:
#     #     access=giveMeARandomAccessButAccessible(croi.numberCroix)#which way
#     #     croi.goPickUp(access,robot,builderCollector)#recup
#     #     gestionDepotA.realizeFirstDepotAvaible(robot,builderCollector)#depot
    
#     # #realisations des dispensers
#     # for disp in dispensers:
#     #     disp.goPickUpBalls(1,robot,waterDispenser)
#     #     gestionShootA.placeAndDoTheShot(robot,waterDispenser,disp.numberDispenser)

#    # actions = gimmeARandomStackOfActionsButPossibleAndInAConsistantOrder(robot,builderCollector,waterDispenser,ordre,croix,depots,ordreD,dispensers,shoots)
#     actions = logicalActionStackHardMade
#     #print(actions)
    actions = getHarcodedStackOfAction(side,rm,robot,builderCollector,waterDispenser)
    while len(actions)!=0:
        act = actions.pop()
        if(act.typ!=Treatment.emptyTyp):
            currentPosXY=robot.get_position()[:2]
            path = rm.get_shortest_path( currentPosXY , act.actionPoint )
            AutomateTools.myPurepursuite(robot,path)
            act()



runAutomate('B',b,g,w)
b.stop()