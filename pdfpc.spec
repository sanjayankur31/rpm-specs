Name:           pdfpc
Version:        4.0.0
Release:        2%{?dist}
Summary:        A GTK based presentation viewer application for GNU/Linux

License:        GPLv2+
URL:            http://davvil.github.io/%{name}/
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires:  libgee-devel poppler-glib-devel cmake gtk3-devel
BuildRequires:  librsvg2-devel vala-devel gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel

%description
pdfpc is a GTK based presentation viewer application for GNU/Linux which uses
Keynote like multi-monitor output to provide meta information to the speaker
during the presentation. It is able to show a normal presentation window on one
screen, while showing a more sophisticated overview on the other one providing
information like a picture of the next slide, as well as the left over time
till the end of the presentation. The input files processed by pdfpc are PDF
documents, which can be created using nearly any of today's presentation
software.

%prep
%setup -q -n %{name}-v%{version}


%build
%cmake -DSYSCONFDIR=/etc .
make %{?_smp_mflags}


%install
%make_install


%files
%doc README.rst CHANGELOG.txt
%{_bindir}/%{name}
%license LICENSE.txt
%config(noreplace) %{_sysconfdir}/%{name}rc
%{_mandir}/man1/%{name}*
%{_datadir}/pixmaps/%{name}


%changelog
* Sat Jun 20 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.0.0-2
- Had forgotten license
- https://bugzilla.redhat.com/show_bug.cgi?id=1232273#c1

* Mon Jun 15 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.0.0-1
- New version

* Mon Jun 15 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.1.1-1
- Initial rpm build
