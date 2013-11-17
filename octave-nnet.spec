%global octpkg nnet

Name:           octave-%{octpkg}
Version:        0.1.13
Release:        3%{?dist}
Summary:        A feed forward multi-layer neural network
Group:          Applications/Engineering
License:        GPLv2+
URL:            http://octave.sourceforge.net/%{octpkg}/
Source0:        http://downloads.sourceforge.net/octave/%{octpkg}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  octave-devel

Requires:       octave
Requires(post): octave
Requires(postun): octave
Obsoletes:      octave-forge <= 20090607

%description
A neural network package for Octave! Goal is to be as compatible as possible to
the one of MATLAB(TM)

%prep
%setup -q -n %{octpkg}

# correct wrong end of line encoding errors
find ./doc/ -name "*" -exec  sed -i 's/\r//' '{}' \;

# remove perl files
# upstream seems to use them for generating docs
rm -rvf ./doc/latex/perl

%build
%octave_pkg_build

%install
rm -rf %{buildroot}
%octave_pkg_install


%post
%octave_cmd pkg rebuild

%preun
%octave_pkg_preun

%postun
%octave_cmd pkg rebuild

%files
%dir %{octpkgdir}
%{octpkgdir}/*.m
%doc COPYING
%doc %{octpkgdir}/doc-cache 
%doc %{octpkgdir}/doc
%{octpkgdir}/packinfo

%changelog
* Tue Aug 14 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.13-3
- Added COPYING to doc

* Tue Aug 14 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.13-2
- Remove perl modules rhbz#847952

* Tue Aug 14 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.13-1
- Initial rpmbuild

