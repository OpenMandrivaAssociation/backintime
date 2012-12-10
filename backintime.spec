%define name  backintime
%define version 1.0.8
%define release %mkrel 1

Summary:    Backup tool for Linux
Name:       %{name}
Version:    %{version}
Release:    %{release}
Source0:    http://backintime.le-web.org/download/backintime/%{name}-%{version}_src.tar.gz
License:    GPLv2
Group:      Archiving/Backup
URL:        http://backintime.le-web.org
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-BuildRoot

%description
Back In Time is a simple backup tool for Linux inspired from 
Flyback project and TimeVault.

#--------------------------------------------------------------------
%package common
Summary: Back Up Tool for Linux
Group: Archiving/Backup
Requires: python
Requires: rsync
Requires: cron-daemon

%description common
Common files for Back In Time

%files common -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/common/
%{_datadir}/%{name}/plugins/
%{_mandir}/man1/%{name}.*
%doc %{_datadir}/doc/%{name}/
%doc %{_datadir}/doc/%{name}-common/

#--------------------------------------------------------------------

%package gnome
Summary: Gnome Frontend for Back In Time
Group:  Archiving/Backup
Requires: pygtk2.0-libglade
Requires: gnome-python
Requires: meld
Requires: python-notify
Requires: %{name}-common = %{version}
Conflicts: %{name}-common < 0.9.24-3

%description gnome
Gnome Frontend for Back In Time.

%files gnome
%defattr(-,root,root,-)
%doc LICENSE README
%{_bindir}/%{name}-gnome
%{_bindir}/backintime-gnome-root
%{_sbindir}/backintime-gnome-root
%{_mandir}/man1/%{name}-gnome.*
%{_sysconfdir}/pam.d/backintime-gnome-root
%{_sysconfdir}/security/console.apps/backintime-gnome-root
%{_datadir}/applications/%{name}-gnome.desktop
%{_datadir}/applications/%{name}-gnome-root.desktop
%{_datadir}/%{name}/gnome/
%doc %{_datadir}/gnome/help/%{name}/
%{_datadir}/omf/%{name}/

#---------------------------------------------------------------------

%package kde4
Summary: KDE Frontend for Back In Time
Group: Archiving/Backup
Requires: x11-tools
Requires: python-kde4 >= 4.1
Requires: kompare
Requires: kdebase4-runtime
Requires: %{name}-common = %version

%description kde4
KDE Frontend for Back In Time.

%files kde4
%defattr(-,root,root,-)
%doc LICENSE README
%{_bindir}/%{name}-kde4
%{_bindir}/backintime-kde4-root
%{_sbindir}/backintime-kde4-root
%{_sysconfdir}/pam.d/backintime-kde4-root
%{_sysconfdir}/security/console.apps/backintime-kde4-root
%{_datadir}/applications/kde4/%{name}-kde4.desktop
%{_datadir}/applications/kde4/%{name}-kde4-root.desktop
%{_datadir}/backintime/kde4/
%doc %{_datadir}/doc/kde4/HTML/en/%{name}/

#---------------------------------------------------------------------

# Let's start the creation of packages

%prep
%setup -q

# Editing backintime-gnome desktop file
sed -i 's|Exec=gksu backintime-gnome|Exec=backintime-gnome-root|g'  gnome/%{name}-gnome-root.desktop

# Editing  backintime-kde desktop file
cp kde4/%{name}-kde4.desktop kde4/%{name}-kde4-root.desktop
sed -i 's|Exec=backintime-kde4|Exec=%{_libdir}/kde4/libexec/kdesu backintime-kde4-root|g' kde4/%{name}-kde4-root.desktop
sed -i 's|Name=Back In Time|Name=Back In Time (root)|g'  kde4/%{name}-kde4-root.desktop

%build
##################################
# Building the -common subpackage#
##################################
pushd common
./configure
%make
popd


################################
# Building the -kde4 subpackage#
################################

pushd kde4
./configure --no-check
%make
popd

#################################
# Building the -gnome subpackage#
#################################

pushd gnome
./configure --no-check
%make
popd

%install
rm -rf %{buildroot}


# Installing common subpackage
pushd common
make install \
     INSTALL="install -p" \
     PREFIX="%{_prefix}" \
     DEST="%{buildroot}/%{_prefix}"

# installing kde4 subpackage
pushd ../kde4
make install \
     INSTALL="install -p" \
     PREFIX="%{_prefix}" \
     DEST="%{buildroot}/%{_prefix}"

pushd ../gnome
# installing gnome subpackage
make install \
     INSTALL="install -p" \
     PREFIX="%{_prefix}" \
     DEST="%{buildroot}/%{_prefix}"
# installing langage files
pushd ..

mkdir -p %{buildroot}%{_sbindir}
cp -p %{buildroot}%{_bindir}/%{name}-gnome \
      %{buildroot}%{_sbindir}/%{name}-gnome-root
cp -p %{buildroot}%{_bindir}/%{name}-kde4 \
      %{buildroot}%{_sbindir}/%{name}-kde4-root

ln -s consolehelper \
      %{buildroot}%{_bindir}/%{name}-gnome-root

ln -s consolehelper \
      %{buildroot}%{_bindir}/%{name}-kde4-root

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps/
#
cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/%{name}-gnome-root
USER=root
PROGRAM=%{_sbindir}/%{name}-gnome-root
SESSION=true
EOF
#
cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/%{name}-kde4-root
USER=root
PROGRAM=%{_sbindir}/%{name}-kde4-root
SESSION=true
EOF

mkdir -p %{buildroot}%{_sysconfdir}/pam.d

cat << EOF > %{buildroot}%{_sysconfdir}/pam.d/%{name}-gnome-root
#%PAM-1.0
auth            include         config-util
account         include         config-util
session         include         config-util
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/pam.d/%{name}-kde4-root
#%PAM-1.0
auth            include         config-util
account         include         config-util
session         include         config-util
EOF


%find_lang %{name}
%clean
rm -rf %{buildroot}



%changelog
* Thu Sep 29 2011 Andrey Bondrov <abondrov@mandriva.org> 1.0.8-1mdv2012.0
+ Revision: 701915
- New version: 1.0.8

* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.26-4mdv2011.0
+ Revision: 616695
- the mass rebuild of 2010.0 packages

* Thu Oct 22 2009 Frederik Himpe <fhimpe@mandriva.org> 0.9.26-3mdv2010.0
+ Revision: 458961
- Add Fedora patch to fix CVE-2009-3611

* Sun May 24 2009 Funda Wang <fwang@mandriva.org> 0.9.26-2mdv2010.0
+ Revision: 379163
- fix requires on gnome subpackage (bug#51096)

* Tue May 19 2009 Frederik Himpe <fhimpe@mandriva.org> 0.9.26-1mdv2010.0
+ Revision: 377741
- Update to new version 0.9.26
- Fix source URL

* Mon May 18 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.9.24-4mdv2010.0
+ Revision: 377252
- Fix Requires

* Mon May 11 2009 Funda Wang <fwang@mandriva.org> 0.9.24-3mdv2010.0
+ Revision: 374204
- arch-dependent as suggested by kdesu
- add requires
- should be noarch
- move gnome manpage into correct sub package

* Sat May 09 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.9.24-2mdv2010.0
+ Revision: 373903
- import backintime


* Sat May 09 2009 John Balcaen  <mandriva@littleboboy.net> 0.9.24-2mdv2009.0
- switching to kdesu instead of kdesudo (thk to neoclust)

* Fri May 08 2009 John Balcaen <mandriva@littleboboy.net> 0.9.24-1mdv2009.0
 Initial import
