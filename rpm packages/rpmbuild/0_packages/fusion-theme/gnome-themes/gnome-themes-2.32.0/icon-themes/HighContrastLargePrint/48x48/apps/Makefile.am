NULL=

themedir = $(datadir)/icons/HighContrastLargePrint
size = 48x48
context = apps

icondir = $(themedir)/$(size)/$(context)

icon_DATA=	\
		accessories-calculator.png \
		accessories-character-map.png \
		accessories-text-editor.png \
		accessories-dictionary.png \
		advanced-directory.png \
		applets-screenshooter.png \
		ax-applet.png \
		brasero.png \
		charpick.png \
		clock.png \
		display-capplet.png \
		eog.png \
		evince.png \
		evolution.png \
		file-roller.png \
		firefox-icon.png \
		ghex.png \
		gimp.png \
		gkb.png \
		gtkam-camera.png \
		gnome-application-generic.png \
		gnome-audio2.png \
		gnome-calc3.png \
		gnome-ccmime.png \
		gnome-ccscreensaver.png \
		gnome-cd.png \
		gnome-folder-generic.png \
		gnome-grecord.png \
		gnome-home.png \
		gnome-info.png \
		gnome-log.png \
		gnome-logo-icon-transparent.png \
		gnome-mailcheck.png \
		gnome-mini-commander.png \
		gnome-mixer-applet.png \
		gnome-palm.png \
		gnome-panel.png \
		gnome-searchtool-animation-rest.png \
		gnome-searchtool-animation.png \
		gnome-settings-accessibility-keyboard.png \
		gnome-settings-default-applications.png \
		gnome-settings-ui-behavior.png \
		gnome-starthere.png \
		gnome-windows.png \
		gnome-workspace.png \
		gok.png \
		help-browser.png \
		launcher-program.png \
		mozilla-icon.png \
		multimedia-volume-control.png \
		orca.png \
		pidgin.png \
		panel-drawer.png \
		panel-force-quit.png \
		perfmeter.png \
		preferences-desktop-accessibility.png \
		preferences-desktop-font.png \
		preferences-desktop-keyboard.png \
		preferences-desktop-keyboard-shortcuts.png \
		preferences-desktop-locale.png \
		preferences-desktop-sound.png \
		preferences-desktop-theme.png \
		preferences-desktop-wallpaper.png \
		preferences-system-session.png \
		preferences-system-windows.png \
		rhythmbox.png \
		smc.png \
		sound-juicer.png \
		star.png \
		totem.png \
		system-file-manager.png \
		thunderbird-icon.png \
		utilities-terminal.png \
		utilities-system-monitor.png \
		window-capplet.png \
		$(NULL)

EXTRA_DIST=	$(icon_DATA) \
		symlinks.dat

if LEGACY_ICON_MAPPING
install-data-local: install-iconDATA
	(cd $(DESTDIR)$(themedir)/$(size) && $(ICONMAP) -c $(context))
endif

install: install-am
	$(SHELL) $(top_srcdir)/common/mkiconlinks.sh $(srcdir)/symlinks.dat $(DESTDIR)$(icondir) 
 
uninstall-symlinks:
	list=`ls $(DESTDIR)$(icondir)`; for p in $$list; do \
		if test -h $(DESTDIR)$(icondir)/$$p; then \
			rm -f $(DESTDIR)$(icondir)/$$p; \
		fi; \
	done
uninstall-am: uninstall-iconDATA uninstall-symlinks
