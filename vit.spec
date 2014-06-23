Name:           vit
Version:        1.2
Release:        0.1.beta1%{?dist}
Summary:        A minimalist Taskwarrior full-screen terminal interface with Vim key bindings 


License:        GPLv3+
URL:            http://taskwarrior.org
Source0:        http://taskwarrior.org/download/%{name}-%{version}.beta1.tar.gz

# Fix up makefile.in
Patch0:         vit-1.2.beta1-Makefile.patch

BuildArch:      noarch
BuildRequires:  task perl-Curses
Requires:       task

%description
Features:
* Vim key bindings
* uncluttered display
* no mouse
* speed


%prep
%setup -q -n %{name}-%{version}.beta1
%patch0

# Make it look at /etc/, not /prefix/etc/
sed -i-backup "14 s:%prefix%::" vit.pl

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc VERSION AUTHORS CHANGES LICENSE README TODO
%{_bindir}/%{name}
%config(noreplace)%{_sysconfdir}/%{name}-commands
%{_mandir}/man1/%{name}*
%{_mandir}/man5/%{name}*


%changelog
* Mon Jun 23 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.2-0.1.beta1
- Initial rpmbuild

* Mon Jun 23 2014 Ankur Sinha <sanjay.ankur@gmail.com>
- 
