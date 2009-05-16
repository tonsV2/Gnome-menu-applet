#! /usr/bin/env python

"""
todo:
	implement about dialog
	implment change of datafile
	support for .desktop files
	gui for editing menus
	create xsd and validate the datafile
	perhaps support for an include element in the datafile
"""


import gnomeapplet
import gtk
import pygtk
pygtk.require('2.0')
import sys, os
from xml.dom import minidom
import xdg.IconTheme
import xdg.DesktopEntry as d



def on_click(mi):
	os.system(mi.__command + " &")

def create_menuitem_by_ref(ref):
#load entry
	de_path = "/usr/share/app-install/desktop/"
	de = d.DesktopEntry(de_path + ref + ".desktop")
	return snot(de)

def snot(de):
#name
	menuitem = gtk.ImageMenuItem(de.getName())
#tooltip
	menuitem.set_tooltip_text(de.getComment())
#icon
	icon = xdg.IconTheme.getIconPath(de.getIcon(), 22, "gnome", ["png"])
	if icon:
		image = gtk.Image()
		image.set_from_file(icon)
		menuitem.set_image(image)
#command
	menuitem.__command = de.getExec()
	menuitem.connect("activate", on_click)

	return menuitem

def create_menuitem(node):
	ref = node.getAttribute("ref")
	if ref:
		return create_menuitem_by_ref(ref)

	menuitem = gtk.ImageMenuItem(node.getAttribute("name"))

	tooltip = node.getAttribute("tooltip")
	if tooltip:
		menuitem.set_tooltip_text(tooltip)

	icon_name = node.getAttribute("icon")
	# size, theme and filetype shouldnt be hard coded but xdg.Config.icon_size didnt return a size suitable for a menu
	# and xdg.Config.icon_theme returned highcolor which caused getIconData() not to return a path
	icon = xdg.IconTheme.getIconPath(icon_name, 22, "gnome", ["png"])
	if icon:
		image = gtk.Image()
		image.set_from_file(icon)
		menuitem.set_image(image)

	command = node.getAttribute("command")
	if command:
		menuitem.__command = command
		menuitem.connect("activate", on_click)

	return menuitem

def create_menu_directory(node):
	ref = node.getAttribute("ref")
	if ref:
		return create_menu_directory_by_ref(ref)
	return create_menuitem(node)

def create_menu_directory_by_ref(ref):
#load entry
	de_path = "/usr/share/desktop-directories/"
	de = d.DesktopEntry(de_path + ref + ".directory")
	return snot(de)

def create_menu(node):
	menus = []
	for child in node.childNodes:
		if child.localName == "item":
			menus.append(create_menuitem(child))
		if child.localName == "seperator":
			menus.append(gtk.SeparatorMenuItem())
		if child.localName == "menu": #if child.childNodes:
			menuitem = create_menu_directory(child)
			menu = gtk.Menu()
			for mi in create_menu(child):	# for each menuitem
				menu.append(mi)		# append each menuitem to menu
			menuitem.set_submenu(menu)	# set menu as submenu of menuitem
			menus.append(menuitem)
	return menus

def factory(applet, iid):
	doc = minidom.parse("full_gnome.xml")		# parse xml file
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

