#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from buttons import LED_ON_OPCODE, LED_OFF_OPCODE, ButtonCard
from components import MAKE_COMPONENT_EXECUTE_OPCODE
from time    import sleep, time
from threading import Thread, RLock, Event
import subprocess
import os
import sys
_RED    = 1
_GREEN  = 0
_BLUE   = 2
_ORANGE = 3


class ButtonGestureMatch():
    WAITING_TEAM     = 0
    WAITING_ODOMETRY = 1
    WAITING_MATCH    = 2


    def __init__(self,buttons, display, wheelebase, server):
        self.buttons = buttons
        self.display = display
        self.server  = server
        self.wheelebase = wheelebase
        #TODO make network verification 
        self.display.show("Select")
        self.status = ButtonGestureMatch.WAITING_TEAM
        self.buttons.affect(_RED,self.button_back)
        self.buttons.affect(_GREEN, self.button_valid)
        self.buttons.affect(_BLUE, self.button_select)
        self.buttons.affect(_ORANGE, self.button_orange)
        self.buttons.setLedOn(_GREEN)
        self.buttons.setLedOn(_ORANGE)
        self.side = None
        self.lock_stat = RLock()
        self.last_tirret_update = 0
        self.tirret_status = Event()
        self.tirret_lock   = RLock()
        self.launch_flag   = Event()
        self.launch_flag.clear()

    def run(self):
        while not self.launch_flag.is_set():
            time.sleep(0.1)

    def button_red(self):
        Thread(target=self._red).start()

    def _red(self):
        self.lock_stat.acquire()
        if(self.status == ButtonGestureMatch.WAITING_ODOMETRY):
            self.side = None
            self.status =  ButtonGestureMatch.WAITING_TEAM 
            self.buttons.setLedOn(_GREEN)
            self.buttons.setLedOn(_ORANGE)
            self.buttons.setLedOff(_RED)
            self.button
        self.lock_release()

        
    def button_blue(self):
        Thread(target=self._blue).start()
    
    def _blue(self):
        if not self.lock_stat.acquire(blocking=False): return
        if(self.status == ButtonGestureMatch.WAITING_TEAM and not self.side is None ):
            self.status  = ButtonGestureMatch.WAITING_ODOMETRY
            self.buttons.setLedOn(_BLUE)
            self.buttons.setLedOff(_GREEN)
            self.buttons.setLedOff(_ORANGE)
            self.buttons.setLedOff(_RED)
            if(self.side ==0):
                self.buttons.setLedOn(_GREEN)
            if(self.side ==1):
                self.buttons.setLedOn(_ORANGE)
            self.display.show("ODOMETRIE")
            sleep(0.5)


        if(self.status == ButtonGestureMatch.WAITING_ODOMETRY):
            #self.wheeledbase.set_position()
            if self.tirret_status.is_set():
                ButtonGestureMatch.WAITING_ODOMETRY
                for k in range(3):
                    for i in range(3):
                        self.buttons.setLedOn(i)
                    sleep(0.2)
                    for i in range(3):
                        self.buttons.setLedOff(i)
                    sleep(0.2)
            else:
                self.status = ButtonGestureMatch.WAITING_MATCH

        self.lock_release()


    def button_green(self):
        Thread(target=self._green).start()



    def _green(self):
        self.lock_stat.acquire()
        if(self.status == ButtonGestureMatch.WAITING_TEAM):
            self.display.show("GREEN")
            self.buttons.setLedOff(_ORANGE)
            self.buttons.setLedOn(_GREEN)
            self.side = 0
        self.lock_release()
    
    def button_orange(self):
        Thread(target=self._orange).start()
    
    def _orange(self):
        self.lock_stat.acquire()
        if(self.status == ButtonGestureMatch.WAITING_TEAM):
            self.display.show("ORANGE")
            self.buttons.setLedOn(_ORANGE)
            self.buttons.setLedOff(_GREEN)
            self.side = 1
        self.lock_release()

    def tirret(self):
        Thread(target=self._tirret).start()

    def _tirret(self):
        self.lock_stat.acquire()
        if self.status== ButtonGestureMatch.WAITING_MATCH:
            self.launch_flag.set()
        self.lock_stat.release()
        self.tirret_lock.acquire()
        self.tirret_status.set()
        time = time.time()
        self.last_tirret_update = time
        self.tirret_lock.release()
        sleep(0.8)
        if time == self.last_tirret_update:
            self.tirret_status.clear()




class ButtonGestureDemo():
    def __init__(self, buttons, display, server):
        self.buttons = buttons
        self.server = server
        self.last_call = time()
        self.menu_selected = "Menu"
        self.item_selected = 0
        self.display = display
        self.exiting = False
        self.menus_dict = {"Menu": ["Make", "IP", "Git pull","Reboot", "Shutdown", "Exit"],
                           "Make": ["WheeledBase", "WaterShooter", "Display", "Sensors"]}
        self.prog_dict  = {"IP" : self.ip_funct,
                           "Reboot": self.reboot_funct,
                           "Shutdown": self.shutdown_funct,
                           "Git pull": self.pull_funct,
                           "Exit": self.exit_funct,
                           "WheeledBase": lambda : self.make_funct("WheeledBase"),
                           "WaterShooter": lambda : self.make_funct("WaterShooter"),
                           "Display":     lambda : self.make_funct("Display"),
                           "Sensors":     lambda : self.make_funct("Sensors")
                           }
        for i in range(5):
            self.buttons.setLedOn(i)
            sleep(0.1)
        for i in reversed(range(5)):
            self.buttons.setLedOff(i)
            sleep(0.1)

        self.buttons.affect(1,self.button_back)
        self.buttons.affect(0, self.button_valid)
        self.buttons.affect(2, self.button_select)
        self.display.set_message("Menu")
    def ip_funct(self):
        ip = ''
        while not ip:
            proc = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE)
            ip = proc.stdout.strip().decode('utf8')
        self.display.set_message(ip)

    def reboot_funct(self):
        self.display.set_message("Lets restart")
        os.system("reboot")


    def shutdown_funct(self):
        self.display.set_message("Good bye !")
        os.system('shutdown now')

    def make_funct(self,arduino):
        arduino_path = os.path.dirname(os.path.realpath(__file__)) + '/../../arduino/' + arduino.lower()
        self.display.set_message("updating...")
        try:
            self.server.execute(MAKE_COMPONENT_EXECUTE_OPCODE, arduino.lower(), "disconnect",list(),dict())
        except KeyError:
            pass
        subprocess.run(['/usr/bin/make', 'upload_safe', '-C', arduino_path])
        self.reset()

    def pull_funct(self):
        self.display.set_message("pulling...")
        subprocess.run(['/usr/bin/git', '-C', sys.path[0], 'pull', '-f'], stdout=subprocess.PIPE)
        self.reset()

    def exit_funct(self):
        self.display.set_message("Off")
        self.exiting = True

    def reset(self):
        self.menu_selected = "Menu"
        self.item_selected = 0
        self._show()

    def button_back(self):
        Thread(target=self._back).start()

    def button_valid(self):
        Thread(target=self._valid).start()

    def button_select(self):
        Thread(target=self._select).start()

    def _show(self):
        str_to_show = self.menus_dict[self.menu_selected][self.item_selected]
        self.display.set_message(str_to_show)


    def _back(self):
        for menu, menu_item in self.menus_dict.items():
            if self.menu_selected in menu_item:
                self.menu_selected = menu
                self.item_selected = 0

    def _valid(self):
        if time()-self.last_call<0.3 : return
        self.last_call = time()
        if self.menus_dict[self.menu_selected][self.item_selected] in self.menus_dict:
            self.menu_selected = self.menus_dict[self.menu_selected][self.item_selected]
            self.item_selected = 0
            self._show()
        else:
            self.prog_dict[self.menus_dict[self.menu_selected][self.item_selected]]()
        
    
    def _select(self):
        self.item_selected+=1
        if self.item_selected>= len(self.menus_dict[self.menu_selected]):
            self.item_selected=0
        self._show()