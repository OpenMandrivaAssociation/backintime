Summary:	Backup tool for Linux
Name:		backintime
Version:	1.0.34
Release:	2
License:	GPLv2+
Group:		Archiving/Backup
Url:		http://backintime.le-web.org
Source0:	http://backintime.le-web.org/download/backintime/%{name}-%{version}.tar.gz
BuildArch:	noarch

%description
Back In Time is a simple backup tool for Linux inspired from
Flyback project and TimeVault.

#----------------------------------------------------------------------------

%package common
Summary:	Back Up Tool for Linux
Group:		Archiving/Backup
Requires:	python
Requires:	rsync
Requires:	cron-daemon
Requires:	python-keyring

%description common
Common files for Back In Time.

%files common -f %{name}.lang
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/common/
%{_datadir}/%{name}/plugins/
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/%{name}-config.1.*
%doc %{_datadir}/doc/%{name}/
%doc %{_datadir}/doc/%{name}-common/

#----------------------------------------------------------------------------

%package gnome
Summary:	Gnome Frontend for Back In Time
Group:		Archiving/Backup
Requires:	pygtk2.0-libglade
Requires:	gnome-python
Requires:	meld
Requires:	python-notify
Requires:	%{name}-common = %{version}
Conflicts:	%{name}-common < 0.9.24-3

%description gnome
Gnome Frontend for Back In Time.

%files gnome
%doc LICENSE README
%{_bindir}/%{name}-gnome
%{_bindir}/%{name}-gnome-root
%{_sbindir}/%{name}-gnome-root
%{_mandir}/man1/%{name}-gnome.*
%{_sysconfdir}/pam.d/%{name}-gnome-root
%{_sysconfdir}/security/console.apps/%{name}-gnome-root
%{_datadir}/applications/%{name}-gnome.desktop
%{_datadir}/applications/%{name}-gnome-root.desktop
%{_datadir}/%{name}/gnome/
%doc %{_datadir}/gnome/help/%{name}/
%{_datadir}/omf/%{name}/

#----------------------------------------------------------------------------

%package kde4
Summary:	KDE Frontend for Back In Time
Group:		Archiving/Backup
Requires:	x11-tools
Requires:	python-kde4 >= 4.1
Requires:	kompare
Requires:	kdebase4-runtime
Requires:	%{name}-common = %{version}

%description kde4
KDE Frontend for Back In Time.

%files kde4
%doc LICENSE README
%{_bindir}/%{name}-kde4
%{_bindir}/%{name}-kde4-root
%{_sbindir}/%{name}-kde4-root
%{_sysconfdir}/pam.d/%{name}-kde4-root
%{_sysconfdir}/security/console.apps/%{name}-kde4-root
%{_datadir}/applications/kde4/%{name}-kde4.desktop
%{_datadir}/applications/kde4/%{name}-kde4-root.desktop
%{_datadir}/%{name}/kde4/*
%{_datadir}/doc/kde/HTML/en/%{name}/index.docbook
%{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_bindir}/%{name}-askpass
%{_mandir}/man1/%{name}-kde4.1.xz

#----------------------------------------------------------------------------

%prep
%setup -qc

# Editing backintime-gnome desktop file
sed -i 's|Exec=gksu backintime-gnome|Exec=backintime-gnome-root|g' gnome/%{name}-gnome-root.desktop

# Editing  backintime-kde desktop file
cp kde4/%{name}-kde4.desktop kde4/%{name}-kde4-root.desktop
sed -i 's|Exec=backintime-kde4|Exec=%{_libdir}/kde4/libexec/kdesu backintime-kde4-root|g' kde4/%{name}-kde4-root.desktop
sed -i 's|Name=Back In Time|Name=Back In Time (root)|g' kde4/%{name}-kde4-root.desktop

%build
pushd common
./configure
%make
popd

pushd kde4
./configure --no-check
%make
popd

pushd gnome
./configure --no-check
%make
popd

%install
pushd common
make install \
     INSTALL="install -p" \
     PREFIX="%{_prefix}" \
     DEST="%{buildroot}/%{_prefix}"

pushd ../kde4
make install \
     INSTALL="install -p" \
     PREFIX="%{_prefix}" \
     DEST="%{buildroot}/%{_prefix}"

pushd ../gnome
make install \
     INSTALL="install -p" \
     PREFIX="%{_prefix}" \
     DEST="%{buildroot}/%{_prefix}"
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

cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/%{name}-gnome-root
USER=root
PROGRAM=%{_sbindir}/%{name}-gnome-root
SESSION=true
EOF

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

