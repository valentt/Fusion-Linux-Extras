%define release_name Thorium
%define dist_version 14

Summary:	Fusion Liux release files
Name:		fusion-linux-release
Version:	14
Release:	12
License:	GPLv2
Group:		System Environment/Base
URL:		http://fusionlinux.org
Source:		%{name}-%{version}.tar.gz
Obsoletes:	redhat-release
Provides:	redhat-release = %{version}-%{release}
Provides:	system-release = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Conflicts:	fedora-release

%description
Fusion Linux release files such as yum configs and various /etc/ files that
define the release. This package explicitly is a replacement for the 
trademarked release package, if you are unable for any reason to abide by the 
trademark restrictions on that release package.

%package rawhide
Summary:        Rawhide repo definitions
Requires:	fusion-linux-release = %{version}-%{release}
Conflicts:	fedora-release-rawhide

%description rawhide
This package provides the rawhide repo definitions.

%package notes
Summary:	Release Notes
License:	Open Publication
Group:		System Environment/Base
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	fedora-release-notes

%description notes
Fusion Linux release notes package. This package explicitly is a replacement 
for the trademarked release-notes package, if you are unable for any reason
to abide by the trademark restrictions on that release-notes 
package. Please note that there is no actual useful content here.


%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "Fusion Linux release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/fedora-release
echo "cpe://o:generic:generic:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/fedora-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s fedora-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s fedora-release $RPM_BUILD_ROOT/etc/system-release

install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg

install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Install all the keys, link the primary keys to primary arch files
# and to compat generic location
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for arch in i386 x86_64
  do
  ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora-$arch
done
ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-fedora
for arch in sparc sparc64
  do
  ln -s RPM-GPG-KEY-fedora-%{dist_version}-SPARC RPM-GPG-KEY-fedora-$arch
done
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in *repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT/etc/rpm
cat >> $RPM_BUILD_ROOT/etc/rpm/macros.dist << EOF
# dist macros.

%%fedora		%{dist_version}
%%dist		.fc%{dist_version}
%%fc%{dist_version}		1
EOF

%postun
if [ -f "$RPM_BUILD_ROOT/etc/yum.repos.d/dropbox.repo.rpmnew" ]; then
	mv $RPM_BUILD_ROOT/etc/yum.repos.d/dropbox.repo $RPM_BUILD_ROOT/etc/yum.repos.d/dropbox.repo.backup
	mv $RPM_BUILD_ROOT/etc/yum.repos.d/dropbox.repo.rpmnew $RPM_BUILD_ROOT/etc/yum.repos.d/dropbox.repo
    fi
if [ -f "$RPM_BUILD_ROOT/etc/yum.repos.d/scribus.repo.rpmnew" ]; then
	mv $RPM_BUILD_ROOT/etc/yum.repos.d/scribus.repo $RPM_BUILD_ROOT/etc/yum.repos.d/scribus.repo.backup
	mv $RPM_BUILD_ROOT/etc/yum.repos.d/scribus.repo.rpmnew $RPM_BUILD_ROOT/etc/yum.repos.d/scribus.repo
    fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc GPL 
%config %attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%dir /etc/yum.repos.d

%config(noreplace) /etc/yum.repos.d/fusion-linux.repo
%config(noreplace) /etc/yum.repos.d/fedora-chromium.repo
%config(noreplace) /etc/yum.repos.d/fedora-firefox4.repo
%config(noreplace) /etc/yum.repos.d/fedora-gimp.repo
%config(noreplace) /etc/yum.repos.d/dropbox.repo
%config(noreplace) /etc/yum.repos.d/google.repo
%config(noreplace) /etc/yum.repos.d/mintmenu.repo
%config(noreplace) /etc/yum.repos.d/playonlinux.repo
%config(noreplace) /etc/yum.repos.d/scribus.repo
%config(noreplace) /etc/yum.repos.d/skype.repo
%config(noreplace) /etc/yum.repos.d/virtualbox.repo
%config(noreplace) /etc/yum.repos.d/fuduntu.repo

%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%config %attr(0644,root,root) /etc/rpm/macros.dist
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files notes
%defattr(-,root,root,-)
%doc README.Fusion-Linux-Release-Notes

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%changelog
* Sat Mar 17 2011 Valent Turkovic <valent.turkovic@gmail.com> 1.0-7
- initial package for fusion-linux-release
- replaced generic-release.spec with fusion-linux-release.spec
- remove livna.repo package because it conflicts with livna-release
- added fuduntu repo with only few packages
- changed gpgcheck to 0 in skype.repo
- added release notes
- fix in scribus repo file
- delete scribus and dropbox files in pre
- testing creating backup .repo files in %install
- further tweaking of backup
- if loop to check if rpmnew files exists before using mv command
- correct if check
- test if creatin .backup works
