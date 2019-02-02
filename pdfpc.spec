%global commit caf05c6fbebb4b3e4aff6cedbe33a9c93c425077
%global shortcommit %(c=%{commit}; echo ${c:0:7})


Name:           pdfpc
Version:        4.3.1
Release:        3.20190202.git%{shortcommit}%{?dist}
Summary:        A GTK based presentation viewer application for GNU/Linux

License:        GPLv2+
URL:            https://%{name}.github.io/

%if 0
%global git_tag v4.3.1_0
Source0:        https://github.com/%{name}/%{name}/archive/%{git_tag}.tar.gz
%endif

Source0:        https://github.com/%{name}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz 

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gtk3-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libgee-devel
BuildRequires:  pango-devel
BuildRequires:  poppler-glib-devel
BuildRequires:  vala vala-devel

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
%if 0
%autosetup -n %{name}-%{version}_0
%endif

%autosetup -n %{name}-%{commit}

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
%{_mandir}/man5/%{name}*
%{_datadir}/pixmaps/%{name}


%changelog
* Sat Feb 02 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.3.1-3.20190202.gitcaf05c6f
- Try git master branch

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 20 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.3.1-1
- Update to latest release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 08 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.1.2-1
- Update to latest release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 13 2017 Michael J Gruber <mjg@fedoraproject.org> - 4.1-1
- clean up source and setup
- Update to 4.1

* Sat Aug 26 2017 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.0.8-1
- Update to 4.0.8

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 05 2017 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.0.7-1
- Update to new release

* Wed Feb 22 2017 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.0.6-1
- Update to latest upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.0.1-4
- another specfile fix

* Thu Jan 07 2016 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.0.1-3
- specfile fix

* Thu Jan 07 2016 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.0.1-2
- Fix sourceurl to fix build

* Thu Jan 07 2016 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.0.1-1
- update to latest upstream release

* Sat Jun 20 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.0.0-2
- Had forgotten license
- https://bugzilla.redhat.com/show_bug.cgi?id=1232273#c1

* Mon Jun 15 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.0.0-1
- New version

* Mon Jun 15 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.1.1-1
- Initial rpm build
