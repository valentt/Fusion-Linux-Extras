# version and release passed by command-line
Version: 0.30
Release: 1
Name: dockbarx
Group: User Interface/Desktops
License: GPLv3
Summary: Gnome taskbar applet with groupping and group manipulation.
AutoReqProv: no
BuildArch: noarch
Requires: gnome-python2-desktop
Requires: numpy
Requires: libXcomposite
Provides: dockbarx
Source0: http://launchpad.net/dockbar/dockbarx/x.%{version}/+download/%{name}_%{version}.tar.gz

%description
This is a branch (not a fork) of DockBar (a TaskBar with grouping and group manipulation) 	with some extra features added.

%install
rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar -xvf %{SOURCE0} -C $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%post
# run always after installation
#cd /usr/share/community-fedora-remix/kickstarts/
#/usr/share/community-fedora-remix/kickstarts/makeiso.sh
#/usr/bin/gconftool-2/gconftool-2 --load /usr/share/community-fedora-remix/gconf2/one-panel-settings.xml
#/usr/bin/gconftool-2/gconftool-2 --load /usr/share/community-fedora-remix/gconf2/mintMenu.xml

%preun
# on de-install

%postun
# run only when erasing this package


%files
%attr(0755,root,root) /usr/bin/dockbarx.py
%attr(0755,root,root) /usr/bin/dbx_preference.py
%attr(0644,root,root) /usr/lib/bonobo/servers/GNOME_DockBarXApplet.server
%attr(0755,root,root) /usr/share/dockbarx/themes/
%attr(0644,root,root) /usr/share/dockbarx/docs/
%defattr(0644, root, root)
/usr/bin/dockbarx.py
/usr/bin/dbx_preference.py
/usr/lib/bonobo/servers/GNOME_DockBarXApplet.server
/usr/share/dockbarx/themes/default.tar.gz
/usr/share/dockbarx/themes/Gaia.tar.gz
/usr/share/dockbarx/themes/human_bar.tar.gz
/usr/share/dockbarx/themes/minimalistic.tar.gz
/usr/share/dockbarx/themes/new_theme.tar.gz
/usr/share/dockbarx/docs/CHANGELOG
/usr/share/dockbarx/docs/README
/usr/share/dockbarx/docs/Theming_HOWTO

%changelog
* Sat May 22 2010 Valent Turkovic <valent.turkovic@gmail.com> 0.30-1
- first Fedora package
- Previews added! This feature is still in beta state, though. (Enable it from advanced tab in preference dialog)
- Improved looks for the window list.
- Dockbarx has the option to show icons for windows on the current workspace only now. (See advanced tab)
- Wine applications are no longer all grouped together (unless you want them to be, see advanced tab).
- OpenOffice applications can be separated so that you have different group buttons for the applications (writer, calc, etc.). This also makes openoffice use themed icons and as well as being pin-able. (See advanced tab)
- Drag and drop is improved: If you drag anything to an group button with just one open window, the window will be brought up automatically without the need to go to the popup list first. Also, the drop indicator for launchers is made less clumsy and the new look of the popup window make drag and drop through them easier.
- The windows 7 like option "Show popup" for selecting multiple windows is added (see group button tab in preference dialog).  By Robin Burchell.
- Preference dialog is now separated from rest of dockbarx. It can be started either the old way or with the command "dbx_preference.py"
