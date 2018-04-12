#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
#sys.path.append("../Simulator/controle")
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


rm = RoadMap.load('bornibus.ggb')



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
            self.d1.getAction()[0],
            self.shot.getAction()[0],
            self.panel.getAction()[0],
            self.d3.getAction()[0],
            self.shot.getAction()[2],
            self.treatment.getAction()[0],
            ]
        
        self.action_list[Bornibus.ORANGE] = [
            self.d4.getAction()[0],
            self.shot.getAction()[0],
            self.panel.getAction()[0],
            self.d2.getAction()[0],
            self.shot.getAction()[2],
            self.treatment.getAction()[0],
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


    def run(self):
    #     #schema du plateau :
    #     #         3     0       
    #     #  5                    2 
    #     #      4            1    
    #     #
    #     #       TIME*TIME_STEA           B

        self.wheeledbase.set_position(592, 290,0)
        self.wheeledbase.set_position(592,2710,0)
        self.wheeledbase.lookahead.set(200)
        self.wheeledbase.max_linvel.set(500)
        self.wheeledbase.max_angvel.set(6)
        while len(self.action_list[self.side])!=0:
            act = self.action_list[self.side].pop(0)
            if(act.typ!=ShootGestion.emptyTyp):
                currentPosXY=self.wheeledbase.get_position()[:2]
                path = self.roadmap.get_shortest_path( currentPosXY , act.actionPoint )
                print(path)
                AutomateTools.myPurepursuite(self.wheeledbase,path)
                print("Make action {}".format(act.typ))
                act()
                self.wheeledbase.max_linvel.set(500)
                self.wheeledbase.max_angvel.set(6)



automate = Bornibus(Bornibus.ORANGE, rm, b, l, d)
try:
    automate.run()
except:
    d.close_outdoor()
    d.open_indoor()
    d.disable_shaker()
    d.write_trash(126)
    l.set_motor_velocity(0)
b.stop()
