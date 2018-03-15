#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from buttons import LED_ON_OPCODE, LED_OFF_OPCODE, ButtonCard
from time    import sleep, time
from threading import Thread
import subprocess
import os
import sys
class ButtonGesture():
    def __init__(self, buttons, display):
        self.buttons = buttons
        self.last_call = time()
        self.menu_selected = "Menu"
        self.item_selected = 0
        self.display = display
        self.exiting = False
        self.menus_dict = {"Menu": ["Make", "IP", "Git pull","Reboot", "Shutdown", "Exit"],
                           "Make": ["WheeledBase", "WaterSorter", "Display", "Sensors"]}
        self.prog_dict  = {"IP" : self.ip_funct,
                           "Reboot": self.reboot_funct,
                           "Shutdown": self.shutdown_funct,
                           "Git pull": self.pull_funct,
                           "Exit": self.exit_funct,
                           "WheeledBase": lambda : self.make_funct("WheeledBase"),
                           "WaterSorter": lambda : self.make_funct("WaterSorter"),
                           "Display":     lambda : self.make_funct("Display"),
                           "Sensors":     lambda : self.make_funct("Sensors")
                           }
        for i in range(5):
            self.buttons.setLedOn(i)
            sleep(0.1)
        for i in range(5):
            self.buttons.setLedOff(i)
            sleep(0.1)

        self.buttons.affect(2,self.button_back)
        self.buttons.affect(1, self.button_valid)
        self.buttons.affect(0, self.button_select)
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
        print("UPDATE")
        subprocess.run(['/usr/bin/make', 'upload_safe', '-C', arduino_path])
        self.reset()

    def pull_funct(self):
        self.display.set_message("pulling...")
        print(sys.path[0])
        subprocess.run(['/usr/bin/git', '-C', sys.path[0], 'pull', '-f'], stdout=subprocess.PIPE)
        print("PULL")
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
            if self.menus_dict[self.menu_selected] in menu_item:
                self.menu_selected = menu
                self.item_selected = 0

    def _valid(self):
        if time()-self.last_call<0.3 : return
        self.last_call = time()
        # Case of under menu
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
