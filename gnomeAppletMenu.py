#!/usr/bin/env python

import pygtk
import sys
pygtk.require('2.0')

import gnomeapplet
import gtk

from xml.dom import minidom

def on_click(mi):
	print mi.__command

def create_menuitem(node):
	menuitem = gtk.ImageMenuItem(node.getAttribute("name"))

	tooltip = node.getAttribute("tooltip")
	if tooltip:
		menuitem.set_tooltip_text(tooltip)

	icon = node.getAttribute("icon")
	if icon:
		image = gtk.Image()
		image.set_from_file(icon)
		menuitem.set_image(image)

	command = node.getAttribute("command")
	if command:
		menuitem.__command = command
		menuitem.connect("activate", on_click)

	return menuitem

def create_menu(node):
	menus = []
	for child in node.childNodes:
		if child.localName == "item":
			menus.append(create_menuitem(child))
		if child.localName == "seperator":
			menus.append(gtk.SeparatorMenuItem())
		if child.localName == "menu": #if child.childNodes:
			menuitem = create_menuitem(child)
			menu = gtk.Menu()
			for mi in create_menu(child):	# for each menuitem
				menu.append(mi)		# append each menuitem to menu
			menuitem.set_submenu(menu)	# set menu as submenu of menuitem
			menus.append(menuitem)
	return menus

def factory(applet, iid):
	doc = minidom.parse("menu.xml")		# parse xml file
	rootNode = doc.documentElement		# get root element
	menu_bar = gtk.MenuBar()
	for menu in create_menu(rootNode):	# for each menu in list
		menu_bar.append(menu)		# append each menu

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

