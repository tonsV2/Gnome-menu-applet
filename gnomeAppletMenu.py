#!/usr/bin/env python

import pygtk
import sys
pygtk.require('2.0')

import gnomeapplet
import gtk

from xml.dom import minidom#, Node


def create_menu(node):
	for child in node.childNodes:
		menu = gtk.Menu()
		if child.localName == "item":
			menu.append(gtk.MenuItem(child.getAttribute("name")))
		if child.localName == "seperator":
			menu.append(gtk.SeparatorMenuItem())
		if child.localName == "menu": # && child.childNodes: #isnt the && redundant since a menu always have childnodes?
			parent = gtk.MenuItem(child.getAttribute("name"))
			parent.set_submenu(create_menu(child))
	return menu


def factory(applet, iid):
	menu_bar = gtk.MenuBar()
	doc = minidom.parse("menu.xml")
	rootNode = doc.documentElement

	menu = create_menu(rootNode)
	menu_bar.append(menu)

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

