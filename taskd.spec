Name:           taskd
Version:        1.0.0
Release:        6%{?dist}
Summary:        Secure server providing multi-user, multi-client access to task data
Group:          Applications/Productivity
License:        MIT
URL:            http://tasktools.org/projects/taskd.html
Source0:        http://taskwarrior.org/download/%{name}-%{version}.tar.gz
Source1:        taskd.service
Source2:        taskd-config
Source3:        taskd.xml

BuildRequires:  cmake
BuildRequires:  libuuid-devel
BuildRequires:  gnutls-devel
BuildRequires:  shadow-utils


%if 0%{?rhel} && 0%{?rhel} <= 6
# On rhel, we don't need systemd to build.  but we do on fedora.
# ...just to define some macros
%else
BuildRequires:  systemd
%endif

# For certificate generation
Requires:       gnutls-utils

# Systemd requires
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

%description
The Taskserver is a lightweight, secure server providing multi-user,
multi-client access to task data.  This allows true syncing between desktop and
mobile clients.

Users want task list access from multiple devices running software of differing
sophistication levels to synchronize data seamlessly.  Synchronization requires
the ability to exchange transactions between devices that may not have
continuous connectivity, and may not have feature parity.

The Taskserver provides this and builds a framework to go several steps beyond
merely synchronizing data.

%prep
%setup -q %{name}-%{version}
%build
%cmake
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sharedstatedir}/taskd/

# Users will keep their keys here, but we copy some helpful scripts too.
mkdir -p %{buildroot}%{_sysconfdir}/pki/taskd/
cp -a pki/generate* %{buildroot}%{_sysconfdir}/pki/taskd/.

mkdir -p %{buildroot}%{_localstatedir}/log/taskd/

%if 0%{?rhel} && 0%{?rhel} <= 6
# EL6 and earlier needs a sysvinit script
%else
mkdir -p %{buildroot}%{_unitdir}/
cp -a %{SOURCE1} %{buildroot}%{_unitdir}/taskd.service
%endif

mkdir -p %{buildroot}%{_sharedstatedir}/taskd/orgs/
cp -a %{SOURCE2} %{buildroot}%{_sharedstatedir}/taskd/config

mkdir -p %{buildroot}/%{_prefix}/lib/firewalld/services/
cp -a %{SOURCE3} %{buildroot}/%{_prefix}/lib/firewalld/services/

rm -r %{buildroot}%{_datadir}/doc/taskd/

%pre
getent group taskd >/dev/null || groupadd -r taskd
getent passwd taskd >/dev/null || \
    useradd -r -g taskd -d %{_sharedstatedir}/taskd/ -s /sbin/nologin \
    -c "Task Server system user" taskd
exit 0

# Systemd scriptlets
%if 0%{?rhel} && 0%{?rhel} <= 6
# No systemd for el6
%else

%post
%systemd_post taskd.service
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

%preun
%systemd_preun taskd.service

%postun
%systemd_postun_with_restart taskd.service
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

%endif


%files
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/taskd
%{_bindir}/taskdctl
%{_mandir}/man1/taskd.1.*
%{_mandir}/man5/taskdrc.5.*

%{_sysconfdir}/pki/taskd/generate*

# does not need firewalld to function, so we own the directory
%dir %{_prefix}/lib/firewalld/services/
%{_prefix}/lib/firewalld/services/taskd.xml

%dir %attr(0750, taskd, taskd) %{_sysconfdir}/pki/taskd/
%dir %attr(0750, taskd, taskd) %{_localstatedir}/log/taskd/

%dir %attr(0750, taskd, taskd) %{_sharedstatedir}/taskd/
%config(noreplace) %attr(0644, taskd, taskd) %{_sharedstatedir}/taskd/config
%dir %attr(0750, taskd, taskd) %{_sharedstatedir}/taskd/orgs/

%if 0%{?rhel} && 0%{?rhel} <= 6
# No sysvinit files for el6
%else
%{_unitdir}/taskd.service
%endif

%changelog
* Wed Jul 30 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.0.0-6
- add value of HOMEDIR
- add firewall configuration file

* Thu Feb 27 2014 Ralph Bean <rbean@redhat.com> - 1.0.0-5
- Add ?dist to Release.
- Replace __mkdir_p macro with just mkdir -p
- Use "-a" with cp to preserve timestamp.
- Add requirement on gnutls-utils
- Improve creation of taskd user and group.
- Add systemd scriptlets.
- Update permissions on files and dirs.

* Tue Feb 18 2014 Ralph Bean <rbean@redhat.com> - 1.0.0-4
- Sorting out permissions on /var/lib, /var/log, and /etc/pki/taskd

* Mon Feb 17 2014 Ralph Bean <rbean@redhat.com> - 1.0.0-3
- Included default config and pki tools.

* Mon Feb 17 2014 Ralph Bean <rbean@redhat.com> - 1.0.0-2
- Remove duplicate docs.

* Mon Feb 17 2014 Ralph Bean <rbean@redhat.com> - 1.0.0-1
- Initial packaging for COPR.
