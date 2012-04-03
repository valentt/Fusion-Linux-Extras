%global debug_package %{nil}

Summary: Advanced Gnome menu
Name:    mintmenu
Version: 4.9.9
Release: 5.1
License: GPLv2
#BuildArch: noarch
Group:   User Interface/Desktops
Source0: http://packages.linuxmint.com/pool/main/m/mintmenu/%{name}_%{version}.tar.gz

#64 bit issue and shebangs
Patch0: mintmenu-4.9.9_libc_shebangs.patch

#Packagekit and terminal launchers
Patch1: mintmenu-4.9.9_bindings.patch

#Suse branding
Patch2: mintmenu-4.9.9_suse_branding.patch

# move from /usr/lib to /usr/share
Patch3: mintmenu-4.9.9_datadir.patch

URL: https://launchpad.net/mintmenu
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python-devel
Requires: deskbar-applet
Requires: python >= 2.4
Requires: python < 3.0
Requires: pyxdg
Requires: python-gtk
Requires: alacarte
Requires: gconf2
Requires: PackageKit
Requires: python-xdg

%description
An advanced "slab" style menu for Linux. MintMenu supports filtering, 
fovorites, autosession, and many other features.  MintMenu can either be
added to your gnome-panel or launched in its own window.


%prep
%setup -q -n mintmenu

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1



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
install -d -p %{buildroot}/%{_libdir}/bonobo/servers/
install -m 644 -p usr/lib/bonobo/servers/mintMenu.server %{buildroot}/%{_libdir}/bonobo/servers/mintMenu.server


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/mintmenu
%{_libdir}/bonobo
%dir %{_datadir}/linuxmint
%dir %{_datadir}/linuxmint/mintMenu
%{_datadir}/linuxmint/mintMenu/*.*
%dir %{_datadir}/linuxmint/mintMenu/plugins
%{_datadir}/linuxmint/mintMenu/plugins/*


%changelog
* Thu May 9 2010 William Witt <william@witt-family.net> 4.9.9-1
- Version Update


* Thu Mar 18 2010 William Witt <william@witt-family.net> 4.9.4-1
- Version Update

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
