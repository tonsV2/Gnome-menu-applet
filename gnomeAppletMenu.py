#! /usr/bin/env python

"""
About:
	During a project I had to customize the standard menu. The menu applet relies on the xdg standard for menu 
	structure which seems more complex then it needs to be. As an alternative I developed this applet.

License:
	Free for none commercial use...

todo:
	implement about dialog
	implment change of datafile
	gui for editing menus
	create xsd and validate the datafile
	perhaps support for an include element in the datafile
	use attributes to override settings in declared by reference
	automatic downloading of icons
	drag and drop support
	make menuitem factory

bug:
	dont execute command on menu onhover

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
	command = mi.__command + " &"
	if mi.__terminal:
		"gnome-terminal -e " + command
	os.system(command)

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
	icon = xdg.IconTheme.getIconPath(de.getIcon(), 22, "gnome", ["png", "svg", "jpg"])
	if icon:
		image = gtk.Image()
		image.set_from_file(icon)
		menuitem.set_image(image)
#command
	menuitem.__command = de.getExec()
	menuitem.__terminal = de.getTerminal()
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
	icon = xdg.IconTheme.getIconPath(icon_name, 22, "gnome", ["png", "svg", "jpg"])
	if icon:
		image = gtk.Image()
		image.set_from_file(icon)
		menuitem.set_image(image)

	command = node.getAttribute("command")
	if command:
		menuitem.__command = command
		menuitem.connect("activate", on_click)

	terminal = node.getAttribute("terminal")
	if terminal:
		menuitem.__terminal = terminal
	else:
		menuitem.__terminal = False

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
	datafile = "/home/snot/python/menu/full_gnome.xml"
	doc = minidom.parse(datafile)		# parse xml file
	rootNode = doc.documentElement		# get root element
	menu_bar = gtk.MenuBar()
	menu_bar.connect("button_press_event", showMenu, applet)

	for menu in create_menu(rootNode):	# for each menu in list
		menu_bar.append(menu)		# append each menu

	applet.add(menu_bar)
	applet.show_all()
	return True

def showMenu(widget, event, applet):
	if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
		widget.emit_stop_by_name("button_press_event")
		create_rightclick_menu(applet)

def create_rightclick_menu(applet):
	propxml="""
			<popup name="button3">
				<menuitem name="Item 3" verb="About" label="_About" pixtype="stock" pixname="gtk-about"/>
				<!--menuitem name="Item snot" verb="Kill" label="Kill" pixtype="stock" pixname="gtk-about" /-->
			</popup>"""
	verbs = [("About", showAboutDialog), ("Kill", kill)]
	applet.setup_menu(propxml, verbs, None)

def kill(*arguments, **keywords):
	sys.exit()

def showAboutDialog(*arguments, **keywords):
	print "About... dialog"


if len(sys.argv) == 2 and sys.argv[1] == "run-in-window":
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
	gnomeapplet.bonobo_factory("OAFIID:Gnome_Panel_Menu_Factory", gnomeapplet.Applet.__gtype__, "gnome applet menu", "1.0", factory)

