#!/usr/bin/env python

import pygtk
import sys
pygtk.require('2.0')

import gnomeapplet
import gtk

def factory(applet, iid):
	button = gtk.Button()
	button.set_relief(gtk.RELIEF_NONE)
	button.set_label("ExampleButton")
	button.connect("button_press_event", showMenu, applet)
	applet.add(button)
	applet.show_all()
	return True

def showMenu(widget, event, applet):
	if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
		widget.emit_stop_by_name("button_press_event")
		create_menu(applet)

def create_menu(applet):
	propxml="""
			<popup name="button3">
				<menuitem name="Item 3" verb="About" label="_About" pixtype="stock" pixname="gtk-about"/>
				<menuitem name="Item 4" verb="About 2" label="_About2" pixtype="stock" pixname="gtk-about"/>
			</popup>"""
	verbs = [("About", showAboutDialog)]
	applet.setup_menu(propxml, verbs, None)

def showAboutDialog(*arguments, **keywords):
	print "About"
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


