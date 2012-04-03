%global debug_package %{nil}

Summary: Advanced Gnome menu
Name:    mintmenu
Version: 4.9.4
Release: 0%{?dist}
License: GPLv2
BuildArch: noarch
Group:   User Interface/Desktops
Source0: http://packages.linuxmint.com/pool/main/m/mintmenu/%{name}_%{version}.tar.gz

#https://bugs.launchpad.net/mintmenu/+bug/490174
#Patch0: mintmenu-4.9.0_filepaths.patch
#Fedora fix since Fedora doesn't use sudo
Patch1: mintmenu-4.9.0_testscript.patch
#Fedora fix since Fedora doesn't use synaptic
Patch2: mintmenu-4.9.0_packagemanagement.patch
#Fedora branding
Patch3: mintmenu-4.9.0_branding.patch
#https://bugs.launchpad.net/mintmenu/+bug/490174
#Patch4: mintmenu-4.9.0_filepaths_fix2.patch
#Fedora only issue
Patch5: mintmenu-4.9.0_terminal_launcher.patch
#Fix shebangs
Patch6: mintmenu-4.9.0_thewholeshebang.patch
#Fedora only: LinuxMint uses syaptic/apt-get vs. PackageKit
Patch7: mintmenu-4.9.1_packagekit.patch
# move from /usr/lid to datadir
Patch8: mintmenu-4.9.1_datadir.patch
# dl.open does not work on 64bit systems
Patch9: mintmenu-4.9.4_dlopen.patch

URL: https://launchpad.net/mintmenu
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python-devel
Requires: deskbar-applet
Requires: tracker-search-tool
Requires: python >= 2.4
Requires: python < 3.0
Requires: pyxdg
Requires: gnome-python2-gnomedesktop
Requires: pygtk2
Requires: pygtk2-libglade
Requires: alacarte
Requires: GConf2
Requires: system-logos
Requires: PackageKit


%description
An advanced "slab" style menu for Linux. MintMenu supports filtering, 
fovorites, autosession, and many other features.  MintMenu can either be
added to your gnome-panel or launched in its own window.


%prep
%setup -q -n mintmenu

#%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
#%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
#pure python code, no build required


%install
rm -rf %{buildroot}
#clean out questionably liscensed files.
rm -rf %{buildroot}/usr/lib/linuxmint/mintMenu/mint*.png
rm -rf %{buildroot}/usr/lib/linuxmint/mintMenu/mint*.svg

mkdir %{buildroot}
mkdir %{buildroot}/usr
install -d -p %{buildroot}/%{_bindir}/
install -m 755 -p usr/bin/mintmenu %{buildroot}/%{_bindir}/mintmenu
install -d -p %{buildroot}/%{_datadir}/linuxmint
install -d -p %{buildroot}/%{_datadir}/linuxmint/mintMenu
install -m 644 -p usr/lib/linuxmint/mintMenu/*.* %{buildroot}/%{_datadir}/linuxmint/mintMenu/
rm -rf %{buildroot}/%{_datadir}/linuxmint/mintMenu/*.py
rm -rf %{buildroot}/%{_datadir}/linuxmint/mintMenu/*.orig
install -m 755 -p usr/lib/linuxmint/mintMenu/*.py %{buildroot}/%{_datadir}/linuxmint/mintMenu/
install -d -p %{buildroot}/%{_datadir}/linuxmint/mintMenu/plugins
install -m 644 -p usr/lib/linuxmint/mintMenu/plugins/* %{buildroot}/%{_datadir}/linuxmint/mintMenu/plugins/
install -m 755 -p usr/lib/linuxmint/mintMenu/plugins/*.py %{buildroot}/%{_datadir}/linuxmint/mintMenu/plugins/
install -d -p %{buildroot}/%{_prefix}/lib/bonobo/servers/
install -m 644 -p usr/lib/bonobo/servers/mintMenu.server %{buildroot}/%{_prefix}/lib/bonobo/servers/mintMenu.server


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/mintmenu
%{_prefix}/lib/bonobo/servers/mintMenu.server
%dir %{_datadir}/linuxmint
%dir %{_datadir}/linuxmint/mintMenu
%{_datadir}/linuxmint/mintMenu/*.*
%dir %{_datadir}/linuxmint/mintMenu/plugins
%{_datadir}/linuxmint/mintMenu/plugins/*


%changelog
* Tue Mar 9 2010 William Witt <william@witt-family.net> 4.9.4-0
- Upstream version update

* Sat Dec 13 2009 William Witt <william@witt-family.net> 4.9.1-6
- internal testing

* Sat Dec 13 2009 William Witt <william@witt-family.net> 4.9.1-5
- Final Implementation of PackageKit for package removal

* Sat Dec 13 2009 William Witt <william@witt-family.net> 4.9.1-4
- Test Implementation of PackageKit for package removal

* Sat Dec 13 2009 William Witt <william@witt-family.net> 4.9.1-3
- Test Implementation of PackageKit for package removal

* Sat Dec 13 2009 William Witt <william@witt-family.net> 4.9.1-2
- Test Implementation of PackageKit for package removal

* Sat Dec 13 2009 William Witt <william@witt-family.net> 4.9.1-1
- Test Implementation of PackageKit for package removal

* Fri Dec 4 2009 William Witt <william@witt-family.net> 4.9.1-0
- New version from upsteam:
-   Improved gmenu sub-category items detection, added python-gnomeapplet 
-   dependency, split other, administration and system tools categories 

* Fri Dec 4 2009 William Witt <william@witt-family.net> 4.9.0-12
- Do not disturb timestamps

* Tue Dec 1 2009 William Witt <william@witt-family.net> 4.9.0-11
- back to no arch, moved no arch files to _datadir

* Tue Dec 1 2009 William Witt <william@witt-family.net> 4.9.0-10
- back to no arch, moved no arch files to _datadir

* Mon Nov 30 2009 William Witt <william@witt-family.net> 4.9.0-9
- fix shebang issue from rpmlint

* Sun Nov 30 2009 William Witt <william@witt-family.net> 4.9.0-8
- removed noarch for use of libdir macro for bonobo
- used sed-fu to allow libdir macro to work with python code

* Sun Nov 29 2009 William Witt <william@witt-family.net> 4.9.0-7
- internal testing

* Sun Nov 29 2009 William Witt <william@witt-family.net> 4.9.0-6
- internal testing

* Sun Nov 29 2009 William Witt <william@witt-family.net> 4.9.0-5
- Create clean up spec file and make noarch

* Sun Nov 29 2009 William Witt <william@witt-family.net> 4.9.0-4
- Fix rpmlint errors.

* Sun Nov 29 2009 William Witt <william@witt-family.net> 4.9.0-3
- Fixed terminal not launching from system management plugin bug.

* Sun Nov 29 2009 William Witt <william@witt-family.net> 4.9.0-2
- Added BuildRequires python.  without it, the build fails for .pyo files.

* Sun Nov 29 2009 William Witt <william@witt-family.net> 4.9.0-1
- Modified to keep prestine package from source

* Thu Nov 27 2009 William Witt <william@witt-family.net> 4.9.0-0
- inital creation

