%global tarname 128143-faenza

Name:           faenza-fusion-icon-theme
Version:        0.3
Release:        2%{?dist}
Summary:        Icon theme designed for Fusion Linux Fedora Remix

Group:          User Interface/Desktops 
License:        GPL+
URL:            http://gnome-look.org/content/show.php/Faenza?content=128143
Source0:        http://iso.linux.hr/fusion-linux/Faenza_Fusion_Icons.zip
BuildArch:      noarch

%description
Contains icons for Fusion Linux GTK theme

%prep
%setup -q -c %{tarname}-%{version} 
tar xf Faenza-Fusion.tar.gz

%build

%install
rm -rf $RPM_BUILD_ROOT
#cd ./Faenza-Fusion/places/scalable/ && ln -sf distributor-logo-fedora.svg distributor-logo.svg && cd ../../..
#cd ./Faenza-Fusion/places/48/ && ln -sf distributor-logo-fedora.png distributor-logo.png && cd ../../..
#cd ./Faenza-Fusion/places/32/ && ln -sf distributor-logo-fedora.png distributor-logo.png && cd ../../..
#cd ./Faenza-Fusion/places/24/ && ln -sf distributor-logo-fedora.png distributor-logo.png && cd ../../..
#cd ./Faenza-Fusion/places/22/ && ln -sf distributor-logo-fedora.png distributor-logo.png && cd ../../..
#cd ./Faenza-Fusion/places/16/ && ln -sf distributor-logo-fedora.png distributor-logo.png && cd ../../..
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons
cp -a ./Faenza-Fusion/ $RPM_BUILD_ROOT%{_datadir}/icons
chmod 0644 $RPM_BUILD_ROOT%{_datadir}/icons/Faenza-Fusion/index.theme

%clean
rm -rf $RPM_BUILD_ROOT

%post  
touch --no-create %{_datadir}/icons/Faenza-Fusion &>/dev/null ||:


%postun
if [ $1 -eq 0 ] ; then 
        touch --no-create %{_datadir}/icons/Faenza-Fusion &>/dev/null
        gtk-update-icon-cache -q %{_datadir}/icons/Faenza-Fusion &>/dev/null || : 
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/Faenza-Fusion &>/dev/null || :

%files
%defattr(-,root,root,-)
%{_datadir}/icons/Faenza-Fusion/*
%doc COPYING.txt

%changelog
* Wed Feb 16 2011 Valent Turkovic <valent.turkovic@gmail.com> - 0.3-1
- Fixed leftover brown folder-status icons in /status 
- Added new distributor-logo-fusion-linux logo
- Made distributor-logo-fusion-linux default logo

* Mon Dec 16 2010 Valent Turkovic <valent.turkovic@gmail.com> - 0.2-1
- Small update with more icons converted to blue colour

* Tue Nov 09 2010 Valent Turkovic <valent.turkovic@gmail.com> - 0.1-1
- Intial RPM release

* Wed Aug 11 2010 Tajidin Abd <tajidinabd@archlinux.us> - 0.0.6-1
- New Version from upstream

* Tue Aug 10 2010 Tajidin Abd <tajidinabd@archlinux.us> - 0.0.5-5
- Cleaned up files macro
- Modified install macro  with -a option to keep timestamps on files

* Mon Aug 09 2010 Tajidin Abd <tajidinabd@archlinux.us> - 0.0.5-4
- Version number comes from URL
- made corrections to prep macro 

* Sun Aug 08 2010 Tajidin Abd <tajidinabd@arhclinux.us> - 0.0.5-3
- Corrected version number
- Added scriplet
- Corrected unused of macro

* Sun Aug 08 2010 Tajidin Abd <tajidinabd@archlinux.us> - 0.0.5.2-2
- added global tarname macro
- Corrected the License 
- made corrections to scriplets
- deleted redundant characters
- changed permission issues to satisfy rpmlint errors

* Thu Aug 05 2010 Tajidin Abd <tajidinabd@archlinux.us> - 0.0.5.2-1
- Intial RPM release
