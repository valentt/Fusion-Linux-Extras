Name:    remix13
Version: 1.0
Release: 0%{?dist}
License: GPLv2+
Summary: Community Fedora Remix configuration files
Group:   Applications/System
URL: http://fcoremix.wordpress.com/
Source0: http://fcoremix.wordpress.com/%{name}_%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: livecd-tools
Requires: fedora-kickstarts
Requires: GConf2
Requires: gconf-editor

%description
These are kicstart and GNOME configuration files. If you are interested
to see how this Fedora Remix is made then just look into kickstart files.
Feel free to change them and use them in your own Fedora Remixes.

%package -n community-remix-kickstart
Summary:    Community Fedora Remix configuration files
Group:      Applications/System

%description -n community-remix-kickstart
These are kicstart and GNOME configuration files. If you are interested
to see how this Fedora Remix is made then just look into kickstart files.
Feel free to change them and use them in your own Fedora Remixes.

%package -n custom-gnome-settings
Summary:    Community Fedora Remix configuration files
Group:      Applications/System

%description -n custom-gnome-settings
Custom settings that setup Community Fedora Remix

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README AUTHORS NEWS
%dir %{_datadir}/%{name}/

%files -n community-remix-kickstart
%defattr(-,root,root,-)
%doc COPYING README AUTHORS NEWS
%{_datadir}/%{name}/*.ks

%files -n custom-gnome-settings
%defattr(-,root,root,-)
%doc COPYING README AUTHORS NEWS
%{_datadir}/%{name}/*.xml



%changelog
* Mon May 22 2010 Valent Turkovic <valent.turkovic@gmail.com> 1.0-0
- first build

