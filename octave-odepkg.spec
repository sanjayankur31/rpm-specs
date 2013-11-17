%global octpkg odepkg

Name:           octave-%{octpkg}
Version:        0.8.2
Release:        2%{?dist}
Summary:        A package for solving ordinary differential equations and more

# Most source files are GPLv2+
# A few source files are BSD in src/daskr
License:        GPLv2+ and BSD
URL:            http://octave.sourceforge.net/odepkg/
Source0:        http://downloads.sourceforge.net/octave/%{octpkg}-%{version}.tar.gz

BuildRequires:  octave-devel

Requires:       octave(api) = %{octave_api}
Requires(post): octave
Requires(postun): octave
Obsoletes:      octave-forge <= 20090607

%description
A package for solving ordinary differential equations and more

%prep
%setup -q -n %{octpkg}-%{version}

# correct wrong end of line encoding errors
iconv -f iso8859-1 -t utf-8 doc/odepkg.texi > doc/odepkg.texi.conv && mv -f doc/odepkg.texi.conv doc/odepkg.texi


%build
%octave_pkg_build
chmod 0644 src/daskr/*

%install
rm -rf %{buildroot}
%octave_pkg_install
iconv -f iso8859-1 -t utf-8 %{buildroot}/%{octpkgdir}/doc.info > %{buildroot}/%{octpkgdir}/doc.info.conv && mv -f %{buildroot}/%{octpkgdir}/doc.info.conv %{buildroot}/%{octpkgdir}/doc.info

%post
%octave_cmd pkg rebuild

%preun
%octave_pkg_preun

%postun
%octave_cmd pkg rebuild

%files
%{octpkglibdir}
%dir %{octpkgdir}
%{octpkgdir}/*.m
%{octpkgdir}/packinfo

%doc %{octpkgdir}/doc-cache
%doc %{octpkgdir}/doc.info
%doc %{octpkgdir}/doc
%doc COPYING

%changelog
* Wed Oct 24 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.8.2-2
- Added comment for the two licenses
- Correct permissions

* Thu Oct 18 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.8.2-1
- inital rpm build

