#!/usr/bin/env python

import pygtk
import sys
pygtk.require('2.0')

import gnomeapplet
import gtk

from xml.dom import minidom


def create_menu(node):
	menus = []
	for child in node.childNodes:
		if child.localName == "item":
			menus.append(gtk.MenuItem(child.getAttribute("name")))
		if child.localName == "seperator":
			menus.append(gtk.SeparatorMenuItem())
		if child.localName == "menu": #if child.childNodes:
			menuitem = gtk.MenuItem(child.getAttribute("name"))
			menu = gtk.Menu()
			for mi in create_menu(child):	# for each menuitem
				menu.append(mi)		# append each menuitem to menu
			menuitem.set_submenu(menu)	# set menu as submenu of menuitem
			menus.append(menuitem)
	return menus

def factory(applet, iid):
	doc = minidom.parse("menu.xml")
	rootNode = doc.documentElement
	menu_bar = gtk.MenuBar()
	for menu in create_menu(rootNode):	# for each menu in list
		menu_bar.append(menu)	# append each menu

	applet.add(menu_bar)
	applet.show_all()
	return True


if len(sys.argv) == 2:
	if sys.argv[1] == "run-in-window":
		mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		mainWindow.set_title("Gnome Applet Menu")
		mainWindow.connect("destroy", gtk.main_quit)
		applet = gnomeapplet.Applet()
		factory(applet, None)
		applet.reparent(mainWindow)
		mainWindow.show_all()
		gtk.main()
		sys.exit()

if __name__ == '__main__':
	print "Starting factory"
	gnomeapplet.bonobo_factory("OAFIID:Gnome_Panel_Menu_Factory", gnomeapplet.Applet.__gtype__, "gnome applet menu", "0.1", factory)


def create_menu_old():
	menu = gtk.Menu()

	menu.append(gtk.MenuItem("Open"))
	menu.append(gtk.MenuItem("Save"))
	menu.append(gtk.SeparatorMenuItem())
	menu.append(gtk.MenuItem("_Exit"))

	menuItemFile = gtk.MenuItem("Applications")
	menuItemFile.set_submenu(menu)

	menu2 = gtk.Menu()
	menu2.append(gtk.ImageMenuItem("Open"))
	menu2.append(gtk.MenuItem("Save"))
	menu2.append(gtk.SeparatorMenuItem())
	menu2.append(gtk.MenuItem("Exit"))

	menuItemFile2 = gtk.MenuItem("Places")
	menuItemFile2.set_submenu(menu2)

	menu_bar = gtk.MenuBar()
#	menu_bar.append(menuItemFile)
#	menu_bar.append(menuItemFile2)


	doc = minidom.parse("menu.xml")
	rootNode = doc.documentElement
	menu_bar.append(rec_xml(rootNode))

	return menu_bar

