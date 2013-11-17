Summary:        Dockapp with moving eyes that follow mouse movement
Summary(de):    Dockapp mit einem Augenpaar, das dem Mauszeiger folgt
Name:           wmeyes
Version:        1.2
Release:        3%{?dist}
License:        MIT
Group:          User Interface/X
URL:            http://www.bstern.org/%{name}/
Source0:        http://bstern.org/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.man

BuildRequires:  libXext-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXpm-devel
BuildRequires:  xmkmf

%description
wmeyes is a dockapp with moving eyes that follow mouse movement.
This version also allows execution of a command by clicking the icon.

%description -l de
wmeyes ist ein Dockapp mit einem Augenpaar, das den Bewegungen des Mauszeigers
folgt. Diese Version ermöglicht die Ausführung eines Befehls durch Anklicken
des Symbols.

%prep
%setup -q

%build
cp -p %{SOURCE1} .
xmkmf
make CFLAGS='%{optflags}' %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 755 wmeyes $RPM_BUILD_ROOT%{_bindir}/
install -p -m 644 wmeyes.man $RPM_BUILD_ROOT%{_mandir}/man1/wmeyes.1

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_mandir}/man1/*
%doc ChangeLog README LICENSE


%changelog
* Sun Jul 17 2011 Mario Blättermann <mariobl@fedoraproject.org> 1.2-3
- First packaging for Fedora.
- Fixed BuildRequires.
- Added German summary and description.
- Added CFLAGS.

* Tue Mar 21 2006 J. Krebs <rpm_speedy@yahoo.com> - 1.2-2
- changed prefix path to /usr.

* Thu Mar 24 2005 J. Krebs <rpm_speedy@yahoo.com> - 1.2-1
- Initial build.
