Name:           vit
Version:        1.2
Release:        1%{?dist}
Summary:        A minimalist Taskwarrior full-screen terminal interface with Vim key bindings 


License:        GPLv3+
URL:            http://taskwarrior.org
Source0:        http://taskwarrior.org/download/%{name}-%{version}.tar.gz

# Fix up makefile.in 
# https://bug.tasktools.org/browse/VT-96
Patch0:         vit-1.2-Makefile.patch

# Fix the man page
# https://bug.tasktools.org/browse/VT-97
Patch1:         vit-1.2-manpage5.patch

BuildArch:      noarch
BuildRequires:  task perl(Curses)
Requires:       task

%description
Features:
* Vim key bindings
* uncluttered display
* no mouse
* speed


%prep
%setup -q
%patch0
%patch1

# Make it look at /etc/, not /prefix/etc/
sed -i-backup "14 s:%prefix%::" vit.pl

%build
%configure
make %{?_smp_mflags}


%install
%make_install


%files
%doc AUTHORS CHANGES LICENSE README TODO
%{_bindir}/%{name}
%config(noreplace)%{_sysconfdir}/%{name}-commands
%{_mandir}/man1/%{name}*
%{_mandir}/man5/%{name}*


%changelog
* Fri Jul 11 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.2-1
- Update as per reviewer comments - rhbz1112072

* Tue Jun 24 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.2-1
- Update to new 1.2 stable version

* Mon Jun 23 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.2-0.1.beta1
- Initial rpmbuild

* Mon Jun 23 2014 Ankur Sinha <sanjay.ankur@gmail.com>
- 
