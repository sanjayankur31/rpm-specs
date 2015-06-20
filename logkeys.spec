Name:           logkeys
Version:        0.1.1a
Release:        2%{?dist}
Summary:        Linux keylogger

License:        WTFPL
URL:            http://code.google.com/p/%{name}/
Source0:        http://%{name}.googlecode.com/files/%{name}-%{version}.tar.gz

# Requires ps and dumpkeys for somereason
BuildRequires:  procps kbd

%description
logkeys is a linux keylogger (GNU/Linux systems only). It is no more advanced
than other available linux keyloggers, but is a bit more up to date, it doesn't
unreliably repeat keys and it should never crash your X. All in all, it just
seems to work. It relies on event interface of the Linux input subsystem. Once
set, it logs all common character and function keys, while also being fully
aware of Shift and AltGr key modifiers. It works with serial as well as USB
keyboards. 

%prep
%setup -q

# This shouldn't quite be a build dep. Runtime dependency yes. Build, no.
# Stop configure from looking for /dev/input and /proc/bus/input/devices 
sed -i.backup "3595,3639 d" configure
sed -i.backup -e 's/install-exec-hook//' -e '469,474 d' \
-e "s|-Wall -O3|%optflags|" src/Makefile.in

# Man page error
sed -i.backup 's/^\.\.\.$//' man/logkeys.8

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -vf $RPM_BUILD_ROOT/%{_sysconfdir}/logkeys-*.sh

%files
%doc README COPYING
%{_bindir}/llk
%{_bindir}/llkk
%{_bindir}/logkeys
%{_mandir}/man8/logkeys*

%changelog
* Fri Nov 22 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.1a-2
- Update sourceurl
- Update source0 permissions

* Mon Jan 14 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.1a-2
- Update package as per suggestions in rhbz#799701

* Sun Mar 04 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.1a-1
- Initial rpmbuild
