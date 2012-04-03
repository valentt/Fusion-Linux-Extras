# version and release passed by command-line
Version: 1.6
Release: 2
Name: fusion-linux-14
Group: System Environment/Base
License: GPL
Summary: Fusion Linux Fedora Remix configuration files
AutoReqProv: no
BuildArch: noarch
Requires: coreutils
Requires: GConf2
Provides: fusion-linux-14
Source0: %{name}_%{version}-%{release}.tar.gz

%description
Fusion Linux kickstart files and initial settings
These scripts do setup tasks.

%install
rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar -xvf %{SOURCE0} -C $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%post
# Chromium default settings
mkdir -p /etc/skel/.config/chromium/Default
cp /usr/share/fusion-linux/chromium/Preferences /etc/skel/.config/chromium/Default/
touch /etc/skel/.config/chromium/First\ Run
# GNOME menu applications optimised list
mkdir -p /etc/skel/.config/menus
cp /usr/share/fusion-linux/application-menu/applications.menu /etc/skel/.config/menus/
# install Sensation font
mkdir -p /usr/share/fonts/sensation
cp /usr/share/fusion-linux/fonts/Sansation/* /usr/share/fonts/sensation/
# add fusion-welcome to autostart
ln -s /usr/share/fusion-linux/fusion-welcome/fusion-welcome /usr/bin/
mkdir -p /etc/skel/.config/autostart
cp /usr/share/fusion-linux/fusion-welcome/fusion-welcome-firstrun.desktop /etc/skel/.config/autostart/
# set default browser and mp3 audio file player
mkdir -p /etc/skel/.local/share/applications
cp /usr/share/fusion-linux/applications/defaults.list /etc/skel/.local/share/applications/
cp /usr/share/fusion-linux/applications/mimeapps.list /etc/skel/.local/share/applications/
# default audacious settings
mkdir -p /etc/skel/.config/audacious/
cp /usr/share/fusion-linux/audacious/config /etc/skel/.config/audacious/


%preun
# on de-install

%postun
# run only when erasing this package


%files
#%attr(0755,root,root) /usr/share/fusion-linux/kickstarts/
#%attr(0755,root,root) /usr/share/fusion-linux/gconf2/
#%attr(0755,root,root) /usr/share/fusion-linux/mintMenu/
#%attr(0755,root,root) /usr/share/fusion-linux/rpm/
%defattr(0755, root, root)
/usr/share/fusion-linux/Fusion-Linux-14-Release-Notes.txt
/usr/share/fusion-linux/gconf2/default-panel-settings.xml
/usr/share/fusion-linux/gconf2/dockbarx.xml
/usr/share/fusion-linux/gconf2/mintMenu.xml
/usr/share/fusion-linux/gconf2/one-panel-settings.xml
/usr/share/fusion-linux/gconf2/one-panel-settings-dockbarx.xml

/usr/share/fusion-linux/kickstarts/makeiso.sh
/usr/share/fusion-linux/kickstarts/fusion-14.ks
/usr/share/fusion-linux/kickstarts/fusion-14-base.ks

/usr/share/fusion-linux/mintMenu/applications.list
/usr/share/fusion-linux/chromium/Preferences
/usr/share/fusion-linux/application-menu/applications.menu

/usr/share/fusion-linux/fonts/Sansation/Sansation_Regular.ttf
/usr/share/fusion-linux/fonts/Sansation/Sansation_Light.ttf
/usr/share/fusion-linux/fonts/Sansation/Sansation_Bold.ttf
/usr/share/fusion-linux/fonts/Sansation/Bernd-Montag-License.txt

/usr/share/fusion-linux/fusion-welcome/fusion-welcome
/usr/share/fusion-linux/fusion-welcome/fusion-welcome.desktop
/usr/share/fusion-linux/fusion-welcome/fusion-welcome-firstrun.desktop
/usr/share/fusion-linux/fusion-welcome/fusion-welcome-libs/check-internet-connection
/usr/share/fusion-linux/fusion-welcome/fusion-welcome-libs/dropbox
/usr/share/fusion-linux/fusion-welcome/fusion-welcome-libs/fini
/usr/share/fusion-linux/fusion-welcome/fusion-welcome-libs/install-skype
/usr/share/fusion-linux/fusion-welcome/fusion-welcome-libs/intro
/usr/share/fusion-linux/fusion-welcome/fusion-welcome-libs/redshift
/usr/share/fusion-linux/fusion-welcome/fusion-welcome-libs/sudo
/usr/share/fusion-linux/fusion-welcome/fusion-welcome-libs/yum-update
/usr/share/fusion-linux/fusion-welcome/fusion-welcome-libs/wallpaper

/usr/share/fusion-linux/applications/defaults.list
/usr/share/fusion-linux/applications/mimeapps.list

/usr/share/fusion-linux/audacious/config


%changelog
* Mon Mar 07 2011 Valent Turkovic <valent.turkovic@gmail.com> 1.6-2
- fusion-welcome now runs only once, and disables autostart
- audacious default settings
- ~/.local/share/applications/ defaults.list and mimeapps.list
- added wallpaper fusion-welcome script

* Thu Mar 03 2011 Valent Turkovic <valent.turkovic@gmail.com> 1.5-4
- Added fusion-welcome script
- added fix to copy fusion-welcome in /usr/bin/
- added new Chromium home page http://fusionlinux.org/fusion-linux-14


* Mon Feb 21 2011 Valent Turkovic <valent.turkovic@gmail.com> 1.4-1
- Added Sensation font

* Thu Feb 17 2011 Valent Turkovic <valent.turkovic@gmail.com> 1.3-1
- Added custom applications.menu for GNOME menu apps
- Added First Run for Chromium (touch becuase it is an empty file)

* Wed Feb 16 2011 Valent Turkovic <valent.turkovic@gmail.com> 1.2-1
- Added Chromium Preferenced file with Fusion Linux homepage
- updated mintMenu preference file

* Sun Feb 13 2011 Valent Turkovic <valent.turkovic@gmail.com> 1.1-2
- Release for Fusion Linux 14

* Tue Nov 02 2010 Valent Turkovic <valent.turkovic@gmail.com> 1.1-1
- Release for Fusion Linux 14 RC

* Sat May 22 2010 Valent Turkovic <valent.turkovic@gmail.com> 1.0-1
- Initial release
