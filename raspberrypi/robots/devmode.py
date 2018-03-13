#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from buttons import LED_ON_OPCODE, LED_OFF_OPCODE, ButtonCard
from time    import sleep
import subprocess
import os

class ButtonGesture():
    def __init__(self, buttons, display):
        self.buttons = buttons
        self.menu_selected = "Menu"
        self.item_selected = 0
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
        for i in range(3):
            self.buttons.setLedOn(i)
            sleep(0.1)
        for i in range(3):
            self.buttons.setLedOff(i)
            sleep(0.1)

        self.buttons.affect(RED_BUTTON,self._back)
        self.buttons.affect(GREEN_BUTTON, self._valid)
        self.buttons.affect(BLUE_BUTTON, self._select)

    def ip_funct(self):
        ip = ''
        while not ip:
            proc = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE)
            ip = proc.stdout.strip().decode('utf8')
        display.set_message(ip)

    def reboot_funct(self):
        self.display.set_message("Let's restart !")
        os.system('sudo reboot')

    def shutdown_funct(self):
        self.display.set_message("Good bye !")
        os.system('sudo shutdown now')

    def make_funct(self,arduino):
        arduino_path = os.path.dirname(os.path.realpath(__file__)) + '/../arduino/' + arduino
        self.display.set_message("updating...")
        subprocess.run(['/usr/bin/make', 'upload_safe', '-C', arduino_path])
        self.reset()

    def pull_funct(self):
        self.display.set_message("pulling...")
        subprocess.run(['/usr/bin/git', 'pull', '-f'], stdout=subprocess.PIPE)
        self.reset()

    def exit_funct(self):
        self.set_message("devMode Off")
        self.exiting = True

    def reset(self):
        self.menu_selected = "Menu"
        self.item_selected = 0
        self._show()

    def _show(self):
        str_to_show = self.menus_dict[self.menu_selected][self.item_selected]
        self.display.set_message(str_to_show)


    def _back(self):
        for menu, menu_item in self.menus_dict:
            if self.menus_dict[self.menu_selected] in menu_item:
                self.menu_selected = menu
                self.item_selected = 0

    def _valid(self):
        # Case of under menu
        if self.menus_dict[self.menu_selected][self.item_selected] in self.menus_dict:
            self.menu_selected = self.menus_dict[self.menu_selected][self.item_selected]
            self.item_selected = 0
        else:
            self.prog_dict[self.menus_dict[self.menu_selected][self.item_selected]]()
    
    def _select(self):
        self.item_selected+=1
        if self.item_selected>= len(self.menus_dict[self.menu_selected]):
            self.item_selected=0
        self._show()
