
install:
	cp gnomeAppletMenu.server /usr/lib/bonobo/servers/
#	cp gnomeAppletMenu.py /usr/lib/gnome-applets/
	mkdir ~/.gmenu/
	cp menu.xml ~/.gmenu/
	cp full_gnome.xml ~/.gmenu/
	cp link_bar.xml ~/.gmenu/

