#custom notification icon for missed calls and unread sms
#based on custom cellular signal indicator by bobby budnick
#based on candidtim's myappindicator
#thanks to Jacob Vlijm for his stackexchange post on appindicator

#requires gir1.2-appindicator3-0.1
#requires python-gobject
#now needs ayatana version of gir1.2appindicator

#remove .cache and/or remove icon-cache.kcache to reset icons

import os
import signal
import time
import re
from gi.repository import Gtk as gtk
from gi.repository import AyatanaAppIndicator3 as appindicator
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
        NOTIFICATION_PRE = open("/home/pi/NOTIFICATION_READOUT","r")
        #print (SIGNAL_PRE.read())
#this was most important-have to read after open-read one byte
        NOTIFICATION_MODE = NOTIFICATION_PRE.read(1)
        if NOTIFICATION_MODE < "1":
            #print(message)  
            GObject.idle_add(  
            indicator.set_icon,   
            "/home/pi/KDE.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
        if NOTIFICATION_MODE >= "1":
            #print(message)
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/UNREAD_SMS.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
        if NOTIFICATION_MODE >= "2":
            #print(message)
            GObject.idle_add(
            indicator.set_icon,
            "/home/pi/MISSED_CALL.svg",
            priority=GObject.PRIORITY_DEFAULT
            )
        time.sleep(3)

def quit(source):
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

