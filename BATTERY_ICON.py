#custom cellular signal indicator by bobby budnick
#based on candidtim's myappindicator
#thanks to Jacob Vlijm for his stackexchange post on appindicator

#requires gir1.2-appindicator3-0.1
#requires python-gobject

#was going to create the icon in a script then update in another
#thus controlling simple python scripts with bash
#this does not work because the icon is represented as variable
#so this one script has to handle all icon operations-see below
#it should look for a text file signal from bash to choose image
#1 in the text file for a 1 signal bar image and so on

#this python script uses threads - all in one script
#the bash way would be to use processes - multiple scripts

#technically bash can be threaded also
#but it does not have capability to do systray icons

#technically this python script can read text file signals also
#but this may not be useful for these purposes
#because the icon variable may exist only as a memory structure
#this means it may not be able to written to a text file
#thus some kind of interprocess communication would be needed

#can not create icon and then immediately start update routine
#because to actually draw the icon a gtk thread is started
#so the gobject threads stuff is used to halt/signal the thread

#remove .cache and/or remove icon-cache.kcache to reset icons

import os
import signal
import time
import re
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GObject
from threading import Thread

APPINDICATOR_ID = 'myappindicator'

def main():
    global indicator
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('sample_icon.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    update = Thread(target=icon_update)
    update.setDaemon(True)
    update.start()
    GObject.threads_init()
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def icon_update():
    while True:
        #message = "RUNNNING"
        BATTERY_PRE = open("/home/pi/BATTERY_READOUT","r")
        #print (BATTERY_PRE.read())
#this was most important-have to read after open-read one byte
        BATTERY_MODE = BATTERY_PRE.read(1)
        if BATTERY_MODE < "1":
            #print("less than 1")
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/sample_icon.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
	if BATTERY_MODE >= "1":
            #print("greater than or equal to one")
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/10_PERCENT_BATTERY.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
	if BATTERY_MODE >= "2":
            #print("greater than or equal to 2")
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/20_PERCENT_BATTERY.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
	if BATTERY_MODE >= "3":
            #print(message)
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/30_PERCENT_BATTERY.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
	if BATTERY_MODE >= "4":
            #print(message)
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/40_PERCENT_BATTERY.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
        if BATTERY_MODE >= "5":
            #print(message)
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/50_PERCENT_BATTERY.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
        if BATTERY_MODE >= "6":
            #print(message)
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/60_PERCENT_BATTERY.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
        if BATTERY_MODE >= "7":
            #print(message)
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/70_PERCENT_BATTERY.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
        if BATTERY_MODE >= "8":
            #print(message)
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/80_PERCENT_BATTERY.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
        if BATTERY_MODE >= "9":
            #print(message)
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/90_PERCENT_BATTERY.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
        time.sleep(3)

def quit(source):
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

