Name:       fusion-linux-logos
Version:    14.3
Release:    1%{?dist}
Summary:    Icons and pictures for Fusion Linux

Group:      System Environment/Base
URL:        https://fedorahosted.org/generic-logos/ 
Source0:    http://iso.linux.hr/fusion-linux/fusion-repo/fusion-14/%{name}/%{name}-%{version}.tar.bz2
#The KDE Logo is under a LGPL license (no version statement)
License:    GPLv2 and LGPLv2+
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

Obsoletes:  redhat-logos
Provides:   redhat-logos = %{version}-%{release}
Provides:   system-logos = %{version}-%{release}

Conflicts:  fedora-logos
Conflicts:  generic-logos
Conflicts:  anaconda-images <= 10
Conflicts:  redhat-artwork <= 5.0.5
# For _kde4_* macros:
BuildRequires: kde-filesystem
# For generating the EFI icon
BuildRequires: libicns-utils

%description
The fusion-logos package contains various image files which can be
used by the bootloader, anaconda, and other related tools. It can
be used as a replacement for the fedora-logos package, if you are
unable for any reason to abide by the trademark restrictions on the
fedora-logos package.

%prep
%setup -q
make

%build
#nothing to build

%install
rm -rf %{buildroot}

# should be ifarch i386
mkdir -p %{buildroot}/boot/grub
install -p -m 644 bootloader/splash.xpm.gz %{buildroot}/boot/grub/splash.xpm.gz
# end i386 bits

mkdir -p %{buildroot}%{_datadir}/firstboot/themes/generic
for i in firstboot/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/firstboot/themes/generic
done

#mkdir -p %{buildroot}%{_datadir}/pixmaps/bootloader
#  install -p -m 644 bootloader/fedora.icns %{buildroot}%{_datadir}/pixmaps/bootloader
#done

mkdir -p %{buildroot}%{_datadir}/pixmaps/splash
for i in gnome-splash/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps/splash
done

mkdir -p %{buildroot}%{_datadir}/pixmaps
for i in pixmaps/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps
done

mkdir -p %{buildroot}%{_kde4_iconsdir}/Fedora-KDE/48x48/apps/
install -p -m 644 icons/Fedora/48x48/apps/* %{buildroot}%{_kde4_iconsdir}/Fedora-KDE/48x48/apps/
mkdir -p %{buildroot}%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536
install -p -m 644 ksplash/SolarComet-kde.png %{buildroot}%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge/
for i in plymouth/charge/* ; do
    install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge/
done

# File or directory names do not count as trademark infringement
mkdir -p %{buildroot}%{_datadir}/icons/Fedora/48x48/apps/
mkdir -p %{buildroot}%{_datadir}/icons/Fedora/scalable/apps/
install -p -m 644 icons/Fedora/48x48/apps/* %{buildroot}%{_datadir}/icons/Fedora/48x48/apps/
install	-p -m 644 icons/Fedora/scalable/apps/* %{buildroot}%{_datadir}/icons/Fedora/scalable/apps/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/anaconda
mkdir -p $RPM_BUILD_ROOT%{_datadir}/backgrounds/fusion-linux/4_3
mkdir -p $RPM_BUILD_ROOT%{_datadir}/backgrounds/fusion-linux/5_4
mkdir -p $RPM_BUILD_ROOT%{_datadir}/backgrounds/fusion-linux/16_10
mkdir -p $RPM_BUILD_ROOT%{_datadir}/backgrounds/rei-forever
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties/
install -p -m 644 anaconda/* $RPM_BUILD_ROOT%{_datadir}/anaconda/
install -p -m 644 backgrounds/fusion-linux.xml $RPM_BUILD_ROOT%{_datadir}/backgrounds/fusion-linux/
install -p -m 644 backgrounds/fusion-linux/4_3/* $RPM_BUILD_ROOT%{_datadir}/backgrounds/fusion-linux/4_3/
install -p -m 644 backgrounds/fusion-linux/5_4/* $RPM_BUILD_ROOT%{_datadir}/backgrounds/fusion-linux/5_4/
install -p -m 644 backgrounds/fusion-linux/16_10/* $RPM_BUILD_ROOT%{_datadir}/backgrounds/fusion-linux/16_10/
install -p -m 644 backgrounds/rei-forever/* $RPM_BUILD_ROOT%{_datadir}/backgrounds/rei-forever/
install -p -m 644 backgrounds/desktop-backgrounds-fusion-linux.xml $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties/
install -p -m 644 backgrounds/desktop-backgrounds-rei-forever.xml $RPM_BUILD_ROOT%{_datadir}/gnome-background-properties/

(cd anaconda; make DESTDIR=%{buildroot} install)

#%posty
#touch --no-create %{_datadir}/icons/Fedora || :
#touch --no-create %{_kde4_iconsdir}/Fedora-KDE ||:

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/Fedora || :
touch --no-create %{_kde4_iconsdir}/Fedora-KDE ||:
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/Fedora/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/Fedora || :
  fi
  if [ -f %{_kde4_iconsdir}/Fedora-KDE/index.theme ]; then
    gtk-update-icon-cache --quiet %{_kde4_iconsdir}/Fedora-KDE/index.theme || :
  fi
fi
fi

%posttrans
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/Fedora/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/Fedora || :
  fi
  if [ -f %{_kde4_iconsdir}/Fedora-KDE/index.theme ]; then
    gtk-update-icon-cache --quiet %{_kde4_iconsdir}/Fedora-KDE/index.theme || :
  fi
fi


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING COPYING-kde-logo README
%{_datadir}/firstboot/themes/*
%{_datadir}/anaconda/*
%{_datadir}/backgrounds/*
%{_datadir}/gnome-background-properties/*
%{_datadir}/icons/Fedora/*/apps/*
%{_datadir}/pixmaps/*
%{_datadir}/plymouth/themes/charge/*
%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png
%{_kde4_iconsdir}/Fedora-KDE/
# should be ifarch i386
/boot/grub/splash.xpm.gz
# end i386 bits

%changelog
* Tue Mar 01 2011 Valent Turkovic <valent.turkovic@gmail.com> - 14.3-1
- Finally got RPM to build with new wallpapers included

* Mon Feb 21 2011 Valent Turkovic <valent.turkovic@gmail.com> - 14.2-1
- Added new anaconda header with Fusion text

* Sat Feb 19 2011 Valent Turkovic <valent.turkovic@gmail.com> - 14.1-1
- Added Fusion Linux wallpapers by Hugo and Rei Forever wallpaper

* Sun Feb 06 2011 Valent Turkovic <valent.turkovic@gmail.com> - 14.0.2-1
- based on generic-icons 14.0.2 with small fixes (powered by fusion)

* Tue Nov 30 2010 Valent Turkovic <valent.turkovic@gmail.com> - 14.0.1-1
- initial packaging. Forked from generic-logos, adapted by Hugo <aptitude8@gmail.com> 
  with Kollision icon as Fusion Linux logo.
