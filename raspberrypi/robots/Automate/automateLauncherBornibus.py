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
from gestionInterrupteur_abeille import *

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
class Bornibus:

    cube="cube"
    dispenser = "disp"
    shot = "shot"
    GREEN  = 0
    ORANGE = 1

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


    def __init__(self, side, roadmap, wheeledbase, waterlauncher, watersorter):
        # Save arduinos
        self.wheeledbase   = wheeledbase
        self.waterlauncher = waterlauncher
        self.watersorter   = watersorter

        # Save annexes inf
        self.side    = side
        self.roadmap = roadmap

        # Apply cube obstacle
        self.reset_cube()

        self.action_list = [list(),list()]
        
        # Generate Dispenser
        self.d1 = Dispenser(1,self.roadmap,  self.wheeledbase, self.watersorter)
        self.d2 = Dispenser(2,self.roadmap,  self.wheeledbase, self.watersorter)
        self.d3 = Dispenser(3,self.roadmap,  self.wheeledbase, self.watersorter)
        self.d4 = Dispenser(4,self.roadmap,  self.wheeledbase, self.watersorter)
            
        # Generate buttons
        self.bie   = Abeille(self.side, self.wheeledbase)
        self.panel = Interrupteur(self.side, self.wheeledbase)

        # Generate balls manipulate
        self.treatment = Treatment(self.side, self.roadmap, self.wheeledbase, self.watersorter)
        self.shot      = Shot(self.side, self.roadmap, self.wheeledbase,  self.watersorter, self.waterlauncher)

        # Generate order list

        self.action_list[Bornibus.GREEN] = [
            #self.panel.getAction()[0],
            #self.d1.getAction()[0],
            self.shot.getAction()[0],
            #self.treatment.getAction()[0],
            ]
        




    def reset_cube(self):
        index = 0
        access =1
        croi = CubesSpotPoints(index,rm)    

        index = 1
        access =3
        croi = CubesSpotPoints(index,rm)    

        index = 2
        access =0
        croi = CubesSpotPoints(index,rm)    

        index = 3
        access =3
        croi = CubesSpotPoints(index,rm)    

        index = 4
        access =3
        croi = CubesSpotPoints(index,rm)    

        index = 5
        access=3
        croi = CubesSpotPoints(index,rm)    


    def getHarcodedStackOfAction(self,side,rm,robot,waterLauncher,waterSorter):
        


    #     #schema du plateau : (cube)
    #     #         3     0       
    #     #  5                    2 
    #     #      4            1        
    #     #
    #     #       A           B

    #OBLIGER d'init les cubes ! (pour les points non accessible)
    #---o

    #---

            #schema du plateau : (dispenser)
        #       3          2    
        #                       
        #  4                    1
        #
        #       A           B

        #initilisation des dispenser et shoot
  
#    ---
        # index = 1
        # access=0
        #self.putOnStackDispAction(rm,index,access,logicalActionStackHardMade,robot,waterLauncher,waterSorter)
        
        #self.putOnStackShootAction(rm,side,index,logicalActionStackHardMade,robot,waterLauncher,waterSorter)
        #self.putOnStackTreatmentAction(rm,side,index,logicalActionStackHardMade,robot,waterLauncher,waterSorter)

    #---
        index = 2
        access=0
    #     self.putOnStackDispAction(rm,index,access,logicalActionStackHardMade,robot,waterLauncher,waterSorter)
        
    #   self.putOnStackShootAction(rm,side,index,logicalActionStackHardMade,robot,waterLauncher,waterSorter)
        self.putOnStackTreatmentAction(rm,side,index,logicalActionStackHardMade,robot,waterLauncher,waterSorter)

    # #---
    #     index = 3
    #     access=0
    #     self.putOnStackDispAction(rm,index,access,logicalActionStackHardMade,robot,waterLauncher,waterSorter)
        
    #     self.putOnStackShootAction(rm,side,index,logicalActionStackHardMade,robot,waterLauncher,waterSorter)
    #     self.putOnStackTreatmentAction(rm,side,index,logicalActionStackHardMade,robot,waterLauncher,waterSorter)

    # #---
    #     index = 4
    #     access=0
    #     self.putOnStackDispAction(rm,index,access,logicalActionStackHardMade,robot,waterLauncher,waterSorter)
        
    #     self.putOnStackShootAction(rm,side,index,logicalActionStackHardMade,robot,waterLauncher,waterSorter)
    #     self.putOnStackTreatmentAction(rm,side,index,logicalActionStackHardMade,robot,waterLauncher,waterSorter)
        #---
    #     odometrie_Bas = Odometrie(side,0).getAction(robot,waterLauncher,waterSorter)[0]
    #     logicalActionStackHardMade.append(odometrie_Bas)
    # #---
    #     odometrie_Droit = Odometrie(side,1).getAction(robot,waterLauncher,waterSorter)[0]
    #     logicalActionStackHardMade.append(odometrie_Droit)
    #---
        # actionnerInterrupteur = Interrupteur(side).getAction(robot,waterLauncher,waterSorter)[0]
        # logicalActionStackHardMade.append(actionnerInterrupteur)
    #---
        # actionnerAbeille = Abeille(side).getAction(robot,waterLauncher,waterSorter)[0]
        # logicalActionStackHardMade.append(actionnerAbeille)
  
    #---


    #------------------------------------------
        logicalActionStackHardMade.reverse()
        return logicalActionStackHardMade


    def run(self):
    #     #schema du plateau :
    #     #         3     0       
    #     #  5                    2 
    #     #      4            1    
    #     #
    #     #       A           B

        self.wheeledbase.set_position(592, 290,0)
        self.wheeledbase.lookahead.set(200)
        while len(self.action_list[self.side])!=0:
            act = self.action_list[self.side].pop(0)
            if(act.typ!=ShootGestion.emptyTyp):
                currentPosXY=self.wheeledbase.get_position()[:2]
                path = self.roadmap.get_shortest_path( currentPosXY , act.actionPoint )
                AutomateTools.myPurepursuite(self.wheeledbase,path)
                act()



automate = Bornibus(Bornibus.GREEN, rm, b, l, d)
automate.run()
b.stop()
