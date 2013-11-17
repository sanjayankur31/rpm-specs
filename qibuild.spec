# used in prep
%global githash 365a79b
%global upstream    aldebaran

Name:           qibuild
Version:        1.14
Release:        0.1.beta1.%{githash}%{?dist}
Summary:        Aims to make compilation of cmake-based projects easy

License:        BSD
URL:            https://github.com/aldebaran/qibuild
# wget --content-disposition https://github.com/aldebaran/qibuild/tarball/v1.14-beta1

# The git head is a little more updated, but not yet tagged
Source0:        aldebaran-qibuild-v1.14-beta1-0-g365a79b.tar.gz
Patch0:         qibuild-find-python-sphinx.patch

BuildRequires:  python-sphinx cmake python-devel
#Requires:       

%description
This project aims to make compilation of cmake-based projects easy.
Please refer to the documentation for more information.

qibuild is under a BSD-style license that can be found in the COPYING file.
Any contribution is more than welcome ;)


%prep
%setup -q -n %{upstream}-%{name}-%{githash}
%patch0 -p0


%build
%cmake .
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Place the doc in correct location. Check cmake for any setting on this
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT/%{_datadir}/%{name}/doc $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/ -v
rmdir $RPM_BUILD_ROOT/%{_datadir}/%{name}

%files
%doc AUTHORS COPYING README.rst TODO
%{_datadir}/cmake/qibuild/
%{_mandir}/man1/qi*.gz

%changelog
* Wed Aug 08 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.14-0.1.beta1.365a79b
- Initial rpm build

