#!/usr/bin/python

#   dockbar.py
#
#	Copyright 2008, 2009, 2010 Aleksey Shaferov and Matias Sars
#
#	DockbarX is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	DockbarX is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with dockbar.  If not, see <http://www.gnu.org/licenses/>.


import pygtk
pygtk.require('2.0')
import gtk
import gobject
import sys
import wnck
import gnomeapplet
import os
import dbus
import gio
import keybinder
import gc
import subprocess
from time import time
gc.enable()

from groupbutton import *
from cairowidgets import *
from theme import Theme, NoThemesError
from common import *

import i18n
_ = i18n.language.gettext

VERSION = 'x.0.39.8'


ATOM_WM_CLASS = gtk.gdk.atom_intern("WM_CLASS")

SPECIAL_RES_CLASSES = {
                        'thunderbird-bin': 'thunderbird',
                        'amarokapp': 'amarok',
                        'lives-exe': 'lives',
                        'exaile.py': 'exaile',
                        'eric4.py': 'eric',
                        'geogebra-geogebra': 'geogebra',
                        'tuxpaint.tuxpaint': 'tuxpaint'
                      }

class AboutDialog():
    __instance = None

    def __init__ (self):
        if AboutDialog.__instance is None:
            AboutDialog.__instance = self
        else:
            AboutDialog.__instance.about.present()
            return
        self.about = gtk.AboutDialog()
        self.about.set_name("DockbarX Applet")
        self.about.set_logo_icon_name("dockbarx")
        self.about.set_version(VERSION)
        self.about.set_copyright(
            "Copyright (c) 2008-2009 Aleksey Shaferov and Matias S\xc3\xa4rs")
        self.about.connect("response",self.about_close)
        self.about.show()

    def about_close (self,par1,par2):
        self.about.destroy()
        AboutDialog.__instance = None


class GroupList(list):
    def __init__(self):
        list.__init__(self)

    def __getitem__(self, item):
        # Item can be a identifier, path or index
        if item is None:
            raise KeyError, item
        if isinstance(item, (str, unicode)):
            for group in self:
                if group.identifier == item or \
                   (group.desktop_entry is not None and
                    group.desktop_entry.getFileName() == item):
                    return group
            raise KeyError, item
        return list.__getitem__(self, item)

    def get_identifiers(self):
        identifiers = []
        for group in self:
            if group.identifier:
                identifiers.append(group.identifier)
            else:
                identifiers.append(group.desktop_entry.getFileName())
        return identifiers


class DockBar():
    def __init__(self, applet=None, as_awn_applet=False):
        print "Dockbarx init"
        self.applet = applet
        self.groups = None
        self.windows = None
        self.container = None
        self.theme = None

        self.gkeys = {
                        'gkeys_select_next_group': None,
                        'gkeys_select_previous_group': None,
                        'gkeys_select_next_window': None,
                        'gkeys_select_previous_window': None
                     }

        wnck.set_client_type(wnck.CLIENT_TYPE_PAGER)
        self.screen = wnck.screen_get_default()
        self.root_xid = int(gtk.gdk.screen_get_default().get_root_window().xid)
        self.screen.force_update()

        self.globals = Globals()
        self.globals.connect('theme-changed', self.reload)


        #--- Applet / Window container
        if self.applet is not None:
            self.applet.set_applet_flags(
                            gnomeapplet.HAS_HANDLE|gnomeapplet.EXPAND_MINOR)
            if self.applet.get_orient() == gnomeapplet.ORIENT_DOWN \
            or applet.get_orient() == gnomeapplet.ORIENT_UP:
                self.globals.orient = "h"
                self.container = gtk.HBox()
            else:
                self.globals.orient = "v"
                self.container = gtk.VBox()
            self.applet.add(self.container)
            self.pp_menu_xml = """
           <popup name="button3">
           <menuitem name="About Item" verb="About" stockid="gtk-about" />
           <menuitem name="Preferences" verb="Pref" stockid="gtk-properties" />
           <menuitem name="Reload" verb="Reload" stockid="gtk-refresh" />
           </popup>
            """

            self.pp_menu_verbs = [("About", self.on_ppm_about),
                                  ("Pref", self.on_ppm_pref),
                                  ("Reload", self.reload)]
            self.applet.setup_menu(self.pp_menu_xml, self.pp_menu_verbs,None)
            self.applet_origin_x = -1000
            self.applet_origin_y = -1000
            # background bug workaround
            self.applet.set_background_widget(applet)
            self.applet.show_all()
        else:
            self.container = gtk.HBox()
            self.globals.orient = "h"

        # Wait until the container is realized before adding anything to it.
        if not as_awn_applet:
            gobject.timeout_add(10, self.reload_on_realized)

        if self.applet is not None:
            self.applet.connect("size-allocate",self.on_applet_size_alloc)
            self.applet.connect("change_background", self.on_change_background)
            self.applet.connect("change-orient",self.on_change_orient)
            self.applet.connect("delete-event",self.cleanup)

        self.on_gkeys_changed(dialog=False)
        self.globals.connect('gkey-changed', self.on_gkeys_changed)

    def reload_on_realized(self):
        if self.container.window is None:
            return True
        self.reload()
        return False


    def reload(self, event=None, data=None):
        # Remove all old groupbuttons from container.
        for child in self.container.get_children():
            self.container.remove(child)
        if self.windows:
            # Removes windows and unpinned group buttons
            for win in self.screen.get_windows():
                self.on_window_closed(None, win)
        if self.groups is not None:
            # Removes pinned group buttons
            for group in self.groups:
                group.hide_list()
                group.icon_factory.remove()

        del self.groups
        del self.windows
        if self.theme:
            self.theme.remove()
        gc.collect()

        print "Dockbarx reload"
        self.groups = GroupList()
        self.windows = {}
        # Get the monitor on which dockbarx is.
        gdk_screen = gtk.gdk.screen_get_default()
        win = self.container.window
        if win is not None:
            self.monitor = gdk_screen.get_monitor_at_window(win)
        #--- Generate Gio apps
        self.apps_by_id = {}
        self.app_ids_by_exec = {}
        self.app_ids_by_name = {}
        self.app_ids_by_longname = {}
        self.wine_app_ids_by_program = {}
        for app in gio.app_info_get_all():
            id = app.get_id()
            id = id[:id.rfind('.')].lower()
            name = u""+app.get_name().lower()
            exe = app.get_executable()
            if exe:
                self.apps_by_id[id] = app
                if id[:5] == 'wine-':
                    try:
                        cmd = u""+app.get_commandline().lower()
                    except AttributeError:
                        # Older versions of gio doesn't have get_comandline.
                        cmd = u""
                    if cmd.find('.exe') > 0:
                        program = cmd[:cmd.rfind('.exe')+4]
                        program = program[program.rfind('\\')+1:]
                        self.wine_app_ids_by_program[program] = id
                if name.find(' ')>-1:
                    self.app_ids_by_longname[name] = id
                else:
                    self.app_ids_by_name[name] = id
                if exe not in ('sudo','gksudo',
                                'java','mono',
                                'ruby','python'):
                    if exe[0] == '/':
                        exe = exe[exe.rfind('/')+1:]
                        self.app_ids_by_exec[exe] = id
                    else:
                        self.app_ids_by_exec[exe] = id



        try:
            if self.theme is None:
                self.theme = Theme()
            else:
                self.theme.on_theme_changed()
        except NoThemesError, details:
            print details
            sys.exit(1)

        self.container.set_spacing(self.theme.get_gap())
        self.container.show()

        #--- Initiate launchers
        self.desktop_entry_by_id = {}
        self.d_e_ids_by_exec = {}
        self.d_e_ids_by_name = {}
        self.d_e_ids_by_longname = {}
        self.d_e_ids_by_wine_program = {}

        gconf_pinned_apps = self.globals.get_pinned_apps_from_gconf()


        # Initiate launcher group buttons
        for launcher in gconf_pinned_apps:
            identifier, path = launcher.split(';')
            # Fix for launchers made in previous version of dockbarx
            identifier = identifier.lower()
            if identifier == '':
                identifier = None
            self.add_launcher(identifier, path)
        # Update pinned_apps list to remove any pinned_app that are faulty.
        self.update_pinned_apps_list()

        #--- Initiate windows
        # Initiate group buttons with windows
        for window in self.screen.get_windows():
            self.on_window_opened(self.screen, window)

        self.screen.connect("window-opened", self.on_window_opened)
        self.screen.connect("window-closed", self.on_window_closed)
        self.screen.connect("active-window-changed",
                            self.on_active_window_changed)
        self.screen.connect("viewports-changed",
                            self.on_desktop_changed)
        self.screen.connect("active-workspace-changed",
                            self.on_desktop_changed)

        self.on_active_window_changed(self.screen, None)


    def reset_all_surfaces(self):
        # Removes all saved pixbufs with active glow in groupbuttons
        # iconfactories. Use this def when the looks of active glow
        # has been changed.
        for group in self.groups:
            group.icon_factory.reset_surfaces()

    def all_windowbuttons_update_label_state(self):
        # Updates all window button labels. To be used when
        # settings has been changed for the labels.
        for group in self.groups:
            for winb in group.windows.values():
                winb.update_label_state()

    def update_all_popup_labels(self):
        # Updates all popup windows' titles. To be used when
        # settings has been changed for the labels.
        for group in self.groups:
            group.update_popup_label()


    #### Applet events
    def on_ppm_pref(self,event=None,data=None):
        # Starts the preference dialog
        os.spawnlp(os.P_NOWAIT,'/usr/bin/dbx_preference.py',
                    '/usr/bin/dbx_preference.py')

    def on_ppm_about(self,event,data=None):
        AboutDialog()

    def on_applet_size_alloc(self, widget, allocation):
        if widget.window:
            x,y = widget.window.get_origin()
            if x!=self.applet_origin_x or y!=self.applet_origin_y:
                # Applet and/or panel moved
                self.applet_origin_x = x
                self.applet_origin_y = y
                for group in self.groups:
                    group.on_db_move()

    def on_change_orient(self,arg1,data):
        if self.applet.get_orient() == gnomeapplet.ORIENT_DOWN \
        or self.applet.get_orient() == gnomeapplet.ORIENT_UP:
            self.set_orient('h')
        else:
            self.set_orient('v')

    def set_orient(self, orient):
        for group in self.groups:
            self.container.remove(group.button)
        if self.applet:
            self.applet.remove(self.container)
        self.container.destroy()
        self.container = None
        self.globals.orient = orient
        if orient == 'h':
            self.container = gtk.HBox()
        else:
            self.container = gtk.VBox()
        if self.applet:
            self.applet.add(self.container)
        for group in self.groups:
            self.container.pack_start(group.button, False)
        self.container.set_spacing(self.theme.get_gap())
        if self.globals.settings["show_only_current_desktop"]:
            self.container.show()
            self.on_desktop_changed()
        else:
            self.container.show_all()

    def on_change_background(self, applet, type, color, pixmap):
        applet.set_style(None)
        rc_style = gtk.RcStyle()
        applet.modify_style(rc_style)
        if type == gnomeapplet.COLOR_BACKGROUND:
            applet.modify_bg(gtk.STATE_NORMAL, color)
        elif type == gnomeapplet.PIXMAP_BACKGROUND:
            style = applet.style
            style.bg_pixmap[gtk.STATE_NORMAL] = pixmap
            applet.set_style(style)
        return


    #### Wnck events
    def on_active_window_changed(self, screen, previous_active_window):
        # Sets the right window button and group button active.
        for group in self.groups:
            group.set_has_active_window(False)
        # Activate new windowbutton
        active_window = screen.get_active_window()
        if active_window in self.windows:
            active_group_name = self.windows[active_window]
            active_group = self.groups[active_group_name]
            active_group.set_has_active_window(True)
            window_button = active_group.windows[active_window]
            window_button.set_button_active(True)

    def on_window_closed(self,screen,window):
        if window in self.windows:
            identifier = self.windows[window]
            group = self.groups[identifier]
            group.del_window(window)
            if not group.windows and not group.pinned:
                self.groups.remove(group)
            del self.windows[window]

    def on_window_opened(self,screen,window):
        if window.is_skip_tasklist() \
        or not (window.get_window_type() in [wnck.WINDOW_NORMAL,
                                             wnck.WINDOW_DIALOG]):
            return

        try:
            gdkw = gtk.gdk.window_foreign_new(window.get_xid())
            wm_class_property = gdkw.property_get(ATOM_WM_CLASS)[2].split('\0')
            res_class = u"" + wm_class_property[1].lower()
            res_name  = u"" + wm_class_property[0].lower()
        except:
            res_class = window.get_class_group().get_res_class().lower()
            res_name = window.get_class_group().get_name().lower()
        identifier = res_class
        if identifier == "":
            identifier = res_name
        # Special cases
        if identifier in SPECIAL_RES_CLASSES:
            identifier = SPECIAL_RES_CLASSES[identifier]
        if identifier == "wine" \
        and self.globals.settings['separate_wine_apps']:
            identifier = res_name
            wine = True
        else:
            wine = False
        if identifier.startswith("openoffice.org"):
            identifier = self.get_ooo_app_name(window)
            if self.globals.settings['separate_ooo_apps']:
                window.connect("name-changed", self.on_ooo_window_name_changed)
        self.windows[window] = identifier
        if identifier in self.groups.get_identifiers():
            # This isn't the first open window of this group.
            self.groups[identifier].add_window(window)
            return

        if wine:
            if identifier in self.d_e_ids_by_wine_program:
                desktop_entry_id = self.d_e_ids_by_wine_program[identifier]
            else:
                desktop_entry_id = None
        else:
            desktop_entry_id = self.find_desktop_entry_id(identifier)
        if desktop_entry_id:
            # The window is matching a launcher without open windows.
            desktop_entry = self.desktop_entry_by_id[desktop_entry_id]
            path = desktop_entry.getFileName()
            group = self.groups[path]
            group.set_identifier(identifier)
            group.add_window(window)
            self.update_pinned_apps_list()
            self.remove_desktop_entry_id_from_undefined_list(desktop_entry_id)
        else:
            # First window of a new group.
            app = None
            if wine:
                if res_name in self.wine_app_ids_by_program:
                    app_id = self.wine_app_ids_by_program[res_name]
                    app = self.apps_by_id[app_id]
            else:
                app = self.find_gio_app(identifier)
            if app:
                desktop_entry = self.get_desktop_entry_for_id(app.get_id())
            else:
                desktop_entry = None
            group = self.make_groupbutton(identifier=identifier,
                                          desktop_entry=desktop_entry)
            group.add_window(window)

    def find_desktop_entry_id(self, identifier):
        id = None
        rc = u""+identifier.lower()
        if rc != "":
            if rc in self.desktop_entry_by_id:
                id = rc
                print "Opened window matched with desktop entry on id:", rc
            elif rc in self.d_e_ids_by_name:
                id = self.d_e_ids_by_name[rc]
                print "Opened window matched with desktop entry on name:", rc
            elif rc in self.d_e_ids_by_exec:
                id = self.d_e_ids_by_exec[rc]
                print "Opened window matched with desktop entry on executable:", rc
            else:
                for lname in self.d_e_ids_by_longname:
                    pos = lname.find(rc)
                    if pos>-1: # Check that it is not part of word
                        if rc == lname \
                        or (pos==0 and lname[len(rc)] == ' ') \
                        or (pos+len(rc) == len(lname) \
                        and lname[pos-1] == ' ') \
                        or (lname[pos-1] == ' ' and lname[pos+len(rc)] == ' '):
                            id = self.d_e_ids_by_longname[lname]
                            print "Opened window matched with" + \
                                  " desktop entry on long name:", rc
                            break

            if id is None and rc.find(' ')>-1:
                    rc = rc.partition(' ')[0] # Cut all before space
                    # Workaround for apps
                    # with identifier like this 'App 1.2.3' (name with ver)
                    if rc in self.desktop_entry_by_id:
                        id = rc
                        print "Partial name for open window" + \
                              " matched with id:", rc
                    elif rc in self.d_e_ids_by_name:
                        id = self.d_e_ids_by_name[rc]
                        print "Partial name for open " + \
                              "window matched with name:", rc
                    elif rc in self.d_e_ids_by_exec:
                        id = self.d_e_ids_by_exec[rc]
                        print "Partial name for open window" + \
                              " matched with executable:", rc
        return id

    def find_gio_app(self, identifier):
        app = None
        app_id = None
        rc = u""+identifier.lower()
        if rc != "":
            if rc in self.apps_by_id:
                app_id = rc
                print "Opened window matched with gio app on id:", rc
            elif rc in self.app_ids_by_name:
                app_id = self.app_ids_by_name[rc]
                print "Opened window matched with gio app on name:", rc
            elif rc in self.app_ids_by_exec:
                app_id = self.app_ids_by_exec[rc]
                print "Opened window matched with gio app on executable:", rc
            else:
                for lname in self.app_ids_by_longname:
                    pos = lname.find(rc)
                    if pos>-1: # Check that it is not part of word
                        if rc == lname \
                        or (pos==0 and lname[len(rc)] == ' ') \
                        or (pos+len(rc) == len(lname) \
                        and lname[pos-1] == ' ') \
                        or (lname[pos-1] == ' ' and lname[pos+len(rc)] == ' '):
                            app_id = self.app_ids_by_longname[lname]
                            print "Opened window matched with" + \
                                  " gio app on longname:", rc
                            break
            if not app_id:
                if rc.find(' ')>-1:
                    rc = rc.partition(' ')[0] # Cut all before space
                    print " trying to find as",rc
                    # Workaround for apps
                    # with identifier like this 'App 1.2.3' (name with ver)
                    ### keys()
                    if rc in self.apps_by_id.keys():
                        app_id = rc
                        print " found in apps id list as",rc
                    elif rc in self.app_ids_by_name.keys():
                        app_id = self.app_ids_by_name[rc]
                        print " found in apps name list as",rc
                    elif rc in self.app_ids_by_exec.keys():
                        app_id = self.app_ids_by_exec[rc]
                        print " found in apps exec list as",rc
            if app_id:
                app = self.apps_by_id[app_id]
        return app

    def get_ooo_app_name(self, window):
        # Separates the differnt openoffice applications from each other
        # The names are chosen to match the gio app ids.
        if not self.globals.settings['separate_ooo_apps']:
            return "openoffice.org-writer"
        name = window.get_name().lower()
        for app in ['calc', 'impress', 'draw', 'math']:
            if name.endswith(app):
                return "openoffice.org-" + app.lower()
        else:
            return "openoffice.org-writer"

    def on_ooo_window_name_changed(self, window):
        identifier = None
        for group in self.groups:
            if window in group.windows:
                identifier = group.identifier
                break
        else:
            print "OOo app error: Name changed but no group found."
        if identifier != self.get_ooo_app_name(window):
            self.on_window_closed(self.screen, window)
            self.on_window_opened(self.screen, window)
            if window == self.screen.get_active_window():
                self.on_active_window_changed(self.screen, None)


    #### Desktop events
    def on_desktop_changed(self, screen=None, workspace=None):
        if not self.globals.settings['show_only_current_desktop']:
            return
        for group in self.groups:
            group.update_state()
            group.set_icongeo()
            group.nextlist = None


    #### Groupbuttons
    def make_groupbutton(self, identifier=None, desktop_entry=None,
                         pinned=False, index=None, path=None):
        gb = GroupButton(identifier, desktop_entry, pinned, self.monitor)
        if index is None:
            self.container.pack_start(gb.button, False)
        else:
            # Insterts the button on it's index by removing
            # and repacking the buttons that should come after it
            repack_list = self.groups[index:]
            for group in repack_list:
                self.container.remove(group.button)
            self.container.pack_start(gb.button, False)
            for group in repack_list:
                self.container.pack_start(group.button, False)

        if identifier is None:
            name = path
        else:
            name = identifier
        if index:
            self.groups.insert(index, gb)
        else:
            self.groups.append(gb)


        gb.connect('delete', self.remove_groupbutton)
        gb.connect('identifier-change', self.change_identifier)
        gb.connect('pinned', self.update_pinned_apps_list)
        gb.connect('groupbutton-moved', self.on_groupbutton_moved)
        gb.connect('launcher-dropped', self.on_launcher_dropped)
        gb.connect('edit-launcher-properties', self.edit_launcher)
        gb.connect('unpinned', self.on_unpinned)
        gb.connect('minimize-others', self.on_minimize_others)
        gb.connect('launch-preference', self.on_ppm_pref)
        return gb

    def remove_groupbutton(self, arg, name):
        group = self.groups[name]
        self.groups.remove(group)
        self.update_pinned_apps_list()

    def on_unpinned(self, arg, identifier):
        gb = self.groups[identifier]
        # Reset the desktop_entry in case this was
        # an custom launcher.
        if identifier in self.wine_app_ids_by_program:
            app_id = self.wine_app_ids_by_program[identifier]
            app = self.apps_by_id[app_id]
        else:
            app = self.find_gio_app(identifier)
        if app:
            desktop_entry = self.get_desktop_entry_for_id(app.get_id())
            gb.desktop_entry = desktop_entry
            gb.icon_factory.set_desktop_entry(desktop_entry)
        gb.update_name()
        self.update_pinned_apps_list()

    def on_minimize_others(self, arg, gb):
        for gr in self.dockbar.groups.get_groups():
            if gb != gr:
                for win in gr.windows.get_list():
                    win.minimize()




    #### Launchers
    def add_launcher(self, identifier, path):
        if path[:4] == "gio:":
            # This launcher is from an older version of dockbarx.
            # It will be updated to new form automatically.
            if path[4:] in self.apps_by_id:
                app = self.apps_by_id[path[4:]]
                desktop_entry = self.get_desktop_entry_for_id(app.get_id())
                if desktop_entry is None:
                    return
            else:
                print "Couldn't find gio app for launcher %s"%path
                return
        else:
            try:
                desktop_entry = DesktopEntry(path)
            except ParsingError:
                print "Couldn't add launcher: %s is not an desktop file!" % \
                      path
                return
            except UnboundLocalError:
                print "Couldn't add launcher: path %s doesn't exist" % path
                return

        self.make_groupbutton(identifier=identifier, \
                              desktop_entry=desktop_entry, \
                              pinned=True, path=path)
        if identifier is None:
            id = path[path.rfind('/')+1:path.rfind('.')].lower()
            self.desktop_entry_by_id[id] = desktop_entry
            exe = desktop_entry.getExec()
            if self.globals.settings["separate_wine_apps"] \
            and "wine" in exe and ".exe" in exe:
                # We are interested int the nameoftheprogram.exe part of the
                # executable.
                exe = exe[:exe.rfind('.exe')+4][exe.rfind('\\')+1:].lower()
                self.d_e_ids_by_wine_program[exe] = id
                return
            l = exe.split()
            if l[0] in ('sudo','gksudo', 'gksu',
                        'java','mono',
                        'ruby','python'):
                exe = l[1]
            else:
                exe = l[0]
            exe = exe.rpartition('/')[-1]
            exe = exe.partition('.')[0]
            self.d_e_ids_by_exec[exe] = id

            name = u"" + desktop_entry.getName().lower()
            if name.find(' ')>-1:
                self.d_e_ids_by_longname[name] = id
            else:
                self.d_e_ids_by_name[name] = id

    def on_launcher_dropped(self, arg, path, calling_button):
        # Creates a new launcher with a desktop file located at path.
        # The new launcher is inserted at the right (or under)
        # the group button that the launcher was dropped on.
        try:
            desktop_entry = DesktopEntry(path)
        except Exception, detail:
            print "ERROR: Couldn't read dropped file. Was it a desktop entry?"
            print "Error message:", detail
            return False

        # Try to match the launcher against the groups that aren't pinned.
        id = path[path.rfind('/')+1:path.rfind('.')].lower()
        name = u"" + desktop_entry.getName()
        exe = desktop_entry.getExec()
        if self.globals.settings["separate_wine_apps"] \
        and "wine" in exe and ".exe" in exe.lower():
                exe = exe.lower()
                exe = exe[:exe.rfind('.exe')+4]
                exe = exe[exe.rfind('\\')+1:]
                wine = True
        else:
            wine = False
            l= exe.split()
            if l[0] in ('sudo','gksudo', 'gksu',
                        'java','mono',
                        'ruby','python'):
                exe = l[1]
            else:
                exe = l[0]
            exe = exe[exe.rfind('/')+1:]
            if exe.find('.')>-1:
                exe = exe[:exe.rfind('.')]

        if name.find(' ')>-1:
            lname = name
        else:
            lname = None

        if exe[0] == '/':
            exe = exe[exe.rfind('/')+1:]

        print "New launcher dropped"
        print "id: ", id
        if lname:
            print "long name: ", name
        else:
            print "name: ", name
        print "executable: ", exe
        print
        for gb in self.groups:
            if gb.pinned:
                continue
            identifier = gb.identifier
            rc = u"" + identifier.lower()
            if not rc:
                continue
            if wine:
                if rc == exe:
                    break
                else:
                    continue
            if rc == id:
                break
            if rc == name:
                break
            if rc == exe:
                break
            if lname:
                pos = lname.find(rc)
                if pos>-1: # Check that it is not part of word
                    if (pos==0) and (lname[len(rc)] == ' '):
                        break
                    elif (pos+len(rc) == len(lname)) and (lname[pos-1] == ' '):
                        break
                    elif (lname[pos-1] == ' ') and (lname[pos+len(rc)] == ' '):
                        break
            if rc.find(' ')>-1:
                    rc = rc.partition(' ')[0] # Cut all before space
                    # Workaround for apps
                    # with identifier like this 'App 1.2.3' (name with ver)
                    if rc == id:
                        break
                    elif rc == name:
                        break
                    elif rc == exe:
                        break
        else:
            # No unpinned group could be connected
            # with the new launcher. Id, name and exe will be stored
            # so that it can be checked against new windows later.
            identifier = None

            self.desktop_entry_by_id[id] = desktop_entry
            if wine:
                self.d_e_ids_by_wine_program[exe] = id
            else:
                if lname:
                    self.d_e_ids_by_longname[name] = id
                else:
                    self.d_e_ids_by_name[name] = id
                self.d_e_ids_by_exec[exe] = id

        # Remove existing groupbutton for the same program
        winlist = []
        index = None
        if calling_button in (identifier, path):
            index = self.groups.index(self.groups[calling_button])
        try:
            group = self.groups[identifier]
        except KeyError:
            try:
                group = self.groups[path]
            except KeyError:
                group = None
        if group is not None:
            # Get the windows for repopulation of the new button
            winlist = group.windows.keys()
            # Destroy the group button
            group.popup.destroy()
            group.button.destroy()
            group.winlist.destroy()
            self.groups.remove(group)
        if index is None:
            index = self.groups.index(self.groups[calling_button]) + 1
        self.make_groupbutton(identifier=identifier,
                              desktop_entry=desktop_entry,
                              pinned=True,
                              index=index, path=path)
        self.update_pinned_apps_list()
        for window in winlist:
            self.on_window_opened(self.screen, window)
        return True

    def identifier_dialog(self, identifier=None):
        # Input dialog for inputting the identifier.
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        dialog = gtk.MessageDialog(None,
                                   flags,
                                   gtk.MESSAGE_QUESTION,
                                   gtk.BUTTONS_OK_CANCEL,
                                   None)
        dialog.set_title(_('Identifier'))
        dialog.set_markup('<b>%s</b>'%_("Enter the identifier here"))
        dialog.format_secondary_markup(
            _('You should have to do this only if the program fails to recognice its windows. ')+ \
            _('If the program is already running you should be able to find the identifier of the program from the dropdown list.'))
        #create the text input field
        #entry = gtk.Entry()
        combobox = gtk.combo_box_entry_new_text()
        entry = combobox.get_child()
        if identifier:
            entry.set_text(identifier)
        # Fill the popdown list with the names of all class
        # names of buttons that hasn't got a launcher already
        for gb in self.groups:
            if not gb.pinned:
                combobox.append_text(gb.identifier)
        entry = combobox.get_child()
        #entry.set_text('')
        #allow the user to press enter to do ok
        entry.connect("activate",
                      lambda widget: dialog.response(gtk.RESPONSE_OK))
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label(_('Identifier:')), False, 5, 5)
        hbox.pack_end(combobox)
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            text = entry.get_text()
        else:
            text = ''
        dialog.destroy()
        return text

    def on_groupbutton_moved(self, arg, name, calling_button=None):
        # Moves the button to the right of the calling button.

        #Remove the groupbutton that should be moved
        move_group = self.groups[name]
        self.container.remove(move_group.button)
        self.groups.remove(move_group)

        if calling_button:
            index = self.groups.index(self.groups[calling_button]) + 1
        else:
            print "Error: cant move button without the calling button's name"
            return
        # Insterts the button on it's index by removing
        # and repacking the buttons that should come after it
        repack_list = self.groups[index:]
        for group in repack_list:
            self.container.remove(group.button)
        self.container.pack_start(move_group.button, False)
        for group in repack_list:
            self.container.pack_start(group.button, False)
        self.groups.insert(index, move_group)
        self.update_pinned_apps_list()

    def change_identifier(self, arg=None, path=None, old_identifier=None):
        identifier = self.identifier_dialog(old_identifier)
        if not identifier:
            return False
        winlist = []
        if identifier in self.groups.get_identifiers():
                group = self.groups[identifier]
                # Get the windows for repopulation of the new button
                winlist = group.windows.keys()
                # Destroy the group button
                group.popup.destroy()
                group.button.destroy()
                group.winlist.destroy()
                self.groups.remove(group)
        try:
            group = self.groups[old_identifier]
        except KeyError:
            group = self.groups[path]
        group.set_identifier(identifier)
        for window in winlist:
            self.on_window_opened(self.screen, window)
        self.update_pinned_apps_list()

    def update_pinned_apps_list(self, arg=None):
        # Saves pinned_apps_list to gconf.
        gconf_pinned_apps = []
        for gb in self.groups:
            if not gb.pinned:
                continue
            identifier = gb.identifier
            if identifier is None:
                identifier = ''
            path = gb.desktop_entry.getFileName()
            # Todo: Is there any drawbacks from using encode('utf-8') here?
            gconf_pinned_apps.append(identifier.encode('utf-8') + ';' + path)
        self.globals.set_pinned_apps_list(gconf_pinned_apps)

    def remove_desktop_entry_id_from_undefined_list(self, id):
        self.desktop_entry_by_id.pop(id)
        for l in (self.d_e_ids_by_name,
                  self.d_e_ids_by_exec,
                  self.d_e_ids_by_longname,
                  self.d_e_ids_by_wine_program):
            for key, value in l.items():
                if value == id:
                    l.pop(key)
                    break

    def get_desktop_entry_for_id(self, id):
        # Search for the desktop id first in ~/.local/share/applications
        # and then in XDG_DATA_DIRS/applications
        user_folder = os.environ.get('XDG_DATA_HOME',
                                     os.path.join(os.path.expanduser('~'),
                                                  '.local', 'share'))
        data_folders = os.environ.get("XDG_DATA_DIRS",
                                      '/usr/local/share/:/usr/share/')
        folders = "%s:%s"%(user_folder, data_folders)
        for folder in folders.split(':'):
            dirname = os.path.join(folder, "applications")
            basename = id
            run = True
            while run:
                run = False
                path = os.path.join(dirname, basename)
                if os.path.isfile(path):
                    try:
                        return DesktopEntry(path)
                    except:
                        pass
                # If the desktop file is in asubfolders, the id is formated
                # "[subfoldername]-[basename]", but there can of cource be
                # "-" in basenames or subfoldernames as well.
                if "-" in basename:
                    parts = basename.split('-')
                    for n in range(1, len(parts)):
                        subfolder = "-".join(parts[:n])
                        if os.path.isdir(os.path.join(dirname, subfolder)):
                            dirname = os.path.join(dirname, subfolder)
                            basename = "-".join(parts[n:])
                            run = True
                            break

        return None

    def edit_launcher(self, arg, path, identifier):
        launcher_dir = os.path.join(os.path.expanduser('~'),
                                    '.dockbarx', 'launchers')
        if path:
            if not os.path.exists(path):
                print "Error: file %s doesn't exist."%path
            if not os.path.exists(launcher_dir):
                os.makedirs(launcher_dir)
            new_path = os.path.join(launcher_dir, os.path.basename(path))
            if new_path != path:
                os.system('cp %s %s'%(path, new_path))
        else:
            new_path = os.path.join(launcher_dir, "%s.desktop"%identifier)
        process = subprocess.Popen(['gnome-desktop-item-edit', new_path],
                                   env=os.environ)
        gobject.timeout_add(100, self.wait_for_launcher_editor,
                            process, path, new_path, identifier)

    def wait_for_launcher_editor(self, process, old_path, new_path, identifier):
        if process.poll() != None:
            # Launcher editor closed.
            if os.path.isfile(new_path):
                # Update desktop_entry.
                desktop_entry = DesktopEntry(new_path)
                if identifier:
                    gb = self.groups[identifier]
                else:
                    gb = self.groups[old_path]
                gb.desktop_entry = desktop_entry
                gb.update_name()
                gb.icon_factory.set_desktop_entry(desktop_entry)
                gb.icon_factory.reset_surfaces()
                gb.update_state()
                gb.pinned = True
                self.update_pinned_apps_list()
            return False
        return True
    def cleanup(self,event):
        del self.applet

    #### Keyboard actions
    def on_gkeys_changed(self, arg=None, dialog=True):
        functions = {
                     "gkeys_select_next_group": self.gkey_select_next_group,
                     "gkeys_select_previous_group": \
                                self.gkey_select_previous_group,
                     "gkeys_select_next_window": \
                                self.gkey_select_next_window_in_group,
                     "gkeys_select_previous_window": \
                                self.gkey_select_previous_window_in_group,
                   }
        translations = {
           'gkeys_select_next_group': _('Select next group'),
           'gkeys_select_previous_group': _('Select previous group'),
           'gkeys_select_next_window': _('Select next window in group'),
           'gkeys_select_previous_window': _('Select previous window in group')
                       }
        for (s, f) in functions.items():
            if self.gkeys[s] is not None:
                keybinder.unbind(self.gkeys[s])
                self.gkeys[s] = None
            if not self.globals.settings[s]:
                # The global key is not in use
                continue
            keystr = self.globals.settings['%s_keystr'%s]
            try:
                if keybinder.bind(keystr, f):
                    # Key succesfully bound.
                    self.gkeys[s]= keystr
                    error = False
                else:
                    error = True
                    reason = ""
                    # Keybinder sometimes doesn't unbind faulty binds.
                    # We have to do it manually.
                    try:
                        keybinder.unbind(keystr)
                    except:
                        pass
            except KeyError:
                error = True
                reason = _("The key is already bound elsewhere.")
            if error:
                message = _("Error: DockbarX couldn't set global keybinding '%(keystr)s' for %(function)s.")%{'keystr':keystr, 'function':translations[s]}
                text = "%s %s"%(message, reason)
                print text
                if dialog:
                    md = gtk.MessageDialog(
                            None,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE,
                            text
                                          )
                    md.run()
                    md.destroy()


    def gkey_select_next_group(self, previous=False):
        active_found = False
        gl = self.groups
        # Repeat list twice so we can get
        # back to the first group after the last
        gl = gl + gl
        if previous:
            gl.reverse()
        for gr in gl:
            if gr.hide_list_sid is not None:
                # Hide the popup if it's opened
                # by keyboard shortcut.
                gr.hide_list()
            if gr.has_active_window:
                active_found = True
                continue

            if active_found and gr.windows.get_count() > 0:
                # This is the group we will active.
                # Remove the nextlist just in case
                # action_select was recently used.
                gr.nextlist = None
                gr.action_select_next()
                return

        # No group contained the active window.
        # Activate the topmost window that exists
        # in a group instead.
        windows_stacked = self.screen.get_windows_stacked()
        for win in windows_stacked:
            if win in self.windows:
                aws = self.screen.get_active_workspace()
                wws = win.get_workspace()
                if not self.globals.settings['show_only_current_desktop'] or \
                   (wws is None or aws == wws) and win.is_in_viewport(aws):
                    t = int(time())
                    if wws is not None and aws != wws:
                        win.get_workspace().activate(t)
                    if not win.is_in_viewport(aws):
                        wx,wy,ww,wh = self.window.get_geometry()
                        sw = self.screen.get_width()
                        sh = self.screen.get_height()
                        self.screen.move_viewport(wx - (wx%sw), wy - (wy%sh))
                    win.activate(t)
                    break

    def gkey_select_previous_group(self):
        self.gkey_select_next_group(previous=True)

    def gkey_select_next_window_in_group(self, previous=False):
        for gr in self.groups:
            if gr.has_active_window:
                gr.action_select_next_with_popup(previous=previous)

    def gkey_select_previous_window_in_group(self):
        self.gkey_select_next_window_in_group(previous=True)