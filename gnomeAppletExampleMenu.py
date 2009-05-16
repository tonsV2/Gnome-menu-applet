#! /usr/bin/env python

import commands
import pygtk
import sys
pygtk.require('2.0')

import gnomeapplet
import gtk

num = 0
button = gtk.Button()

def factory(applet, iid):
        global button
#       button = gtk.Button()

        button.set_relief(gtk.RELIEF_NONE)
        button.set_label("")
        image = gtk.Image()
        image.set_from_file("/usr/share/icons/gnome/48x48/devices/gnome-dev-floppy-red.png")
        button.set_image(image)
        button.connect("button_press_event", showMenu, applet)
#       button.connect("clicked", on_button_clicked)
        applet.add(button)
        applet.show_all()
        return True

def on_button_clicked(button, *args):
#       button.emit_stop_by_name("button_press_event")
#       create_menu(applet)
        global num
        if (num%2==0):
                image = gtk.Image()
                image.set_from_file("/usr/share/icons/gnome/48x48/devices/gnome-dev-floppy-red.png")
                button.set_image(image)
                button.set_label("")
        else:
                image = gtk.Image()
                image.set_from_file("/usr/share/icons/gnome/48x48/devices/gnome-dev-floppy-green.png")
                button.set_image(image)
                button.set_label("")
        num=num+1

def showMenu(widget, event, applet):
    if event.button == 1:
        global num
        if (num%2==0):
#               image = gtk.Image()
#               image.set_from_file("/usr/share/icons/gnome/48x48/devices/gnome-dev-floppy-red.png")
#               widget.set_image(image)
#               widget.set_label("")
                menu = [
                        ["Ativar Disquete", doFirst],
                        ["Formatar Disquete", doSecond]]
        else:
#               image = gtk.Image()
#               image.set_from_file("/usr/share/icons/gnome/48x48/devices/gnome-dev-floppy-green.png")
#               widget.set_image(image)
#               widget.set_label("")
                menu = [
                        ["Desativar Disquete", doFirst],
                        ["Acessar o Disquete", doSecond]]
#       num=num+1
        createAndShowMenu(event, menu)
        propxml="""
                        <popup name="button1">
                        <menuitem name="Item 1" verb="About" label="_About" pixtype="stock" pixname="gtk-about"/>
                        <menuitem name="file-unlock"    verb="file-unlock"      label="Unlock File"             pixtype="stock" pixname="revelation-unlock" />
                        <menuitem name="file-lock"      verb="file-lock"        label="Lock File"               pixtype="stock" pixname="revelation-lock" />
                        <menuitem name="file-reload"    verb="file-reload"      label="Reload File"             pixtype="stock" pixname="revelation-reload" />
                        <separator />
                        <menuitem name="revelation"     verb="revelation"       label="Start Revelation"        pixtype="stock" pixname="revelation-revelation" />
                        <menuitem name="prefs"          verb="prefs"            label="Preferences"             pixtype="stock" pixname="gtk-properties" />
                        <menuitem name="about"          verb="about"            label="About"                   pixtype="stock" pixname="gnome-stock-about" />
                        </popup>"""
        verbs = [("About", showAboutDialog)]
        applet.setup_menu(propxml, verbs, None)
        widget.emit_stop_by_name("button_press_event")

def doFirst(widget):
    global button
    global num
    num=num+1
    if (num%2==0):
        image = gtk.Image()
        image.set_from_file("/usr/share/icons/gnome/48x48/devices/gnome-dev-floppy-red.png")
        button.set_image(image)
        button.set_label("")
        commands.getstatusoutput("zenity --info --title='Disquete' --text='Disquete desativado. Pode remove-lo do computador agora.'")
    else:
        image = gtk.Image()
        image.set_from_file("/usr/share/icons/gnome/48x48/devices/gnome-dev-floppy-green.png")
        button.set_image(image)
        button.set_label("")
        commands.getstatusoutput("zenity --info --title='Disquete' --text='Disquete ativado. Pronto para uso! (ou nao)'")

def doSecond(widget):
    print "do second"
def doThird(widget):
    print "do third"

def createAndShowMenu(event, menuItems):
    menu = gtk.Menu()
    for menuItem in menuItems:
        item = gtk.ImageMenuItem(menuItem[0], True)
        item.show()
        item.connect( "activate", *menuItem[1:])
        menu.add(item)
    menu.popup( None, None, None, event.button, event.time )


def create_menu(applet):
        propxml="""
                        <popup name="button3">
                        <menuitem name="Item 3" verb="About" label="_About" pixtype="stock" pixname="gtk-about"/>
                        <menuitem name="file-unlock"    verb="file-unlock"      label="Unlock File"             pixtype="stock" pixname="revelation-unlock" />
                        <menuitem name="file-lock"      verb="file-lock"        label="Lock File"               pixtype="stock" pixname="revelation-lock" />
                        <menuitem name="file-reload"    verb="file-reload"      label="Reload File"             pixtype="stock" pixname="revelation-reload" />
                        <separator />
                        <menuitem name="revelation"     verb="revelation"       label="Start Revelation"        pixtype="stock" pixname="revelation-revelation" />
                        <menuitem name="prefs"          verb="prefs"            label="Preferences"             pixtype="stock" pixname="gtk-properties" />
                        <menuitem name="about"          verb="about"            label="About"                   pixtype="stock" pixname="gnome-stock-about" />
                        </popup>"""
        verbs = [("About", showAboutDialog)]
        applet.setup_menu(propxml, verbs, None)

def showAboutDialog(*arguments, **keywords):
        pass

if len(sys.argv) == 2:
        if sys.argv[1] == "run-in-window":
                mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
                mainWindow.set_title("Ubuntu System Panel")
                mainWindow.connect("destroy", gtk.main_quit)
                applet = gnomeapplet.Applet()
                factory(applet, None)
                applet.reparent(mainWindow)
                mainWindow.show_all()
                gtk.main()
                sys.exit()

if __name__ == '__main__':
        print "Starting factory"
        gnomeapplet.bonobo_factory("OAFIID:Gnome_Panel_Example_Factory", gnomeapplet.Applet.__gtype__, "Simple gnome applet example", "1.0", factory)

