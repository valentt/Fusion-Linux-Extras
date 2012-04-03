# version and release passed by command-line
Version: 1.1
Release: 1
Name: fusion-linux
Group: System Environment/Base
License: GPL
Summary: Fusion Linux Fedora Remix configuration files
AutoReqProv: no
BuildArch: noarch
Requires: coreutils
Requires: GConf2
Provides: fusion-linux
Source0: %{name}_%{version}.tar.gz

%description
Community Fedora Remix kickstart files and initial settings
These scripts do setup tasks.

%install
rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar -xvf %{SOURCE0} -C $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%post
# run always after installation
#cd /usr/share/fusion-linux/kickstarts/
#/usr/share/fusion-linux/kickstarts/makeiso.sh
#/usr/bin/gconftool-2/gconftool-2 --load /usr/share/fusion-linux/gconf2/one-panel-settings.xml
#/usr/bin/gconftool-2/gconftool-2 --load /usr/share/fusion-linux/gconf2/mintMenu.xml

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
/usr/share/fusion-linux/gconf2/default-panel-settings.xml
/usr/share/fusion-linux/gconf2/dockbarx.xml
/usr/share/fusion-linux/gconf2/mintMenu.xml
/usr/share/fusion-linux/gconf2/one-panel-settings.xml
/usr/share/fusion-linux/gconf2/one-panel-settings-dockbarx.xml
/usr/share/fusion-linux/kickstarts/makeiso.sh
/usr/share/fusion-linux/kickstarts/fusion-linux-14.ks
/usr/share/fusion-linux/kickstarts/fusion-linux-14-base.ks
/usr/share/fusion-linux/mintMenu/applications.list
/usr/share/fusion-linux/rpm/autoten-4.5-9.fc12.noarch.rpm
/usr/share/fusion-linux/rpm/community-fedora-remix-1.0-1.noarch.rpm
/usr/share/fusion-linux/rpm/dockbarx-0.30-1.noarch.rpm
/usr/share/fusion-linux/rpm/mintmenu-4.9.9-1.fc13.noarch.rpm

%changelog
* Sun Feb 13 2011 Valent Turkovic <valent.turkovic@gmail.com> 1.1-1
- Release for Fusion Linux 14

* Sat May 22 2010 Valent Turkovic <valent.turkovic@gmail.com> 1.0-1
- Initial release
