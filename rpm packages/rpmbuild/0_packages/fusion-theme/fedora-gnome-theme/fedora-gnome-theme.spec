Summary: Fedora GNOME theme
Name: fedora-gnome-theme
Version: 13.4
Release: 2%{?dist}
BuildArch: noarch
# No version given, no license attribution.
License: GPL+
Group: User Interface/Desktops
# There is no official upstream yet
Source0: %{name}-%{version}.tar.bz2
URL: http://www.redhat.com

Requires: fedora-icon-theme
Requires: dmz-cursor-themes

# we require XML::Parser for our in-tree intltool
BuildRequires: perl(XML::Parser)
BuildRequires: intltool

Obsoletes: redhat-artwork

%description
This package contains the Fedora GNOME meta theme.

%prep
%setup -q

%build
%configure
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

# These are empty
rm -f ChangeLog NEWS README

# The upstream packages may gain po files at some point in the near future
%find_lang %{name} || touch %{name}.lang

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING
%{_sysconfdir}/gtk-2.0/gtkrc
%{_sysconfdir}/gtk-3.0/gtkrc
%{_datadir}/themes/Fedora

%changelog
* Mon Jul 12 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 13.4-2
- drop no longer needed Requires: notification-daemon-engine-slider, it's now
  the default theme in notification-daemon and part of its package, and we
  don't want to drag notification-daemon onto the KDE spin (#605664)

* Thu Jul  1 2010 Matthias Clasen <mclasen@redhat.com> 13.4-1
- Include gtkrc for GTK3

* Tue Jun  1 2010 Matthias Clasen <mclasen@redhat.com> 13.3-1
- Update to match F13 artwork

* Tue Nov 24 2009 Matthias Clasen <mclasen@redhat.com> 13.1-1
- Revert the previous change, since we need the Fedora
  icon theme to drop our start-here icon

* Tue Nov 24 2009 Matthias Clasen <mclasen@redhat.com> 13.0-1
- Drop fedora-icon-theme dep, use Mist directly

* Thu Sep 24 2009 Matthias Clasen <mclasen@redhat.com> 12.3-1
- Use a new notification theme

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> 12.2-1
- Update the gtkrc file too

* Fri Aug 14 2009 Matthias Clasen <mclasen@redhat.com> 12.1-1
- Add cursor theme to the Fedora metatheme

* Fri Aug 07 2009 Adam Jackson <ajax@redhat.com> 12.0-1
- Bump to 12.0
- Add gtk-cursor-theme-name to gtkrc

* Wed Aug  5 2009 Matthias Clasen  <mclasen@redhat.com> - 8.0.0-10
- Match default changes in GConf schemas

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 24 2008 Matthias Clasen  <mclasen@redhat.com> - 8.0.0-7
- Only require bluecurve cursors, not the full icon theme

* Mon Aug 25 2008 Matthias Clasen  <mclasen@redhat.com> - 8.0.0-4
- Use nodoka notification theme (#460045)

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 8.0.0-3
- fix license tag

* Fri May 23 2008 Martin Sourada <martin.sourada@gmail.com> - 8.0.0-2
- Require gtk-nodoka-engine instead of nodoka-theme-gnome (bug 447644)

* Thu Oct 11 2007 Ray Strode <rstrode@redhat.com> - 8.0.0-1
- Update to 8.0.0 to match F8 release

* Wed Oct 10 2007 Ray Strode <rstrode@redhat.com> - 1.0.2-1
- Drop requires for screensaver themes (bug 327161)

* Wed Oct 10 2007 Ray Strode <rstrode@redhat.com> - 1.0.1-1
- Fix up Requires / Obsoletes and theme file

* Tue Sep 25 2007 Ray Strode <rstrode@redhat.com> - 1.0.0-1
- Initial import, version 1.0.0
