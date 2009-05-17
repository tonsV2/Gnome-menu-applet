
install:
	cp gnomeAppletMenu.server /usr/lib/bonobo/servers/
	cp gnomeAppletMenu.py /usr/lib/gnome-panel/
	mkdir ~/.gmenu/
#	cp gnomeAppletMenu.py /usr/share/app
	cp menu.xml ~/.gmenu/
	cp full_gnome.xml ~/.gmenu/
	cp link_bar.xml ~/.gmenu/

