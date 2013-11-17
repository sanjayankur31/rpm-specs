%global commit de0dcf16baaee40f756b9e55656fe2e744bc8fc3
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global stackname std_msgs

Name:           ros-%{stackname}
Version:        0.4.11
Release:        3.20130605git%{shortcommit}%{?dist}
Summary:        Standard ROS Messages

License:        BSD
URL:            http://www.ros.org/wiki/std_msgs
Source0:        https://github.com/ros/%{stackname}/archive/%{commit}/%{stackname}-%{version}-%{shortcommit}.tar.gz
BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  python-setuptools-devel
BuildRequires:  catkin-devel
BuildRequires:  python-genmsg-devel
BuildRequires:  python-gencpp-devel
BuildRequires:  python-genlisp-devel
BuildRequires:  python-genpy-devel

Requires:       python-genpy
Requires:       python-genlisp
Requires:       ros-release

BuildRequires:   common-lisp-controller
Requires:        common-lisp-controller
Requires(post):  common-lisp-controller
Requires(preun): common-lisp-controller

%description
std_msgs contains common message types representing primitive data types and 
other basic message constructs, such as multiarrays.

%package devel
Summary:  Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: roscpp_core-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{stackname}-%{commit}

%build
mkdir build
pushd build
%cmake \
  -DSETUPTOOLS_DEB_LAYOUT=OFF \
  -DCATKIN_BUILD_BINARY_PACKAGE="1" \
  ..
popd

%install
make -C build install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/pkgconfig
mv %{buildroot}%{_libdir}/pkgconfig/%{stackname}.pc %{buildroot}/%{_datadir}/pkgconfig

# Fix lisp extensions
mkdir -m 755 -p %{buildroot}%{_datadir}/common-lisp/source
mkdir -m 755 -p %{buildroot}%{_datadir}/common-lisp/systems

mv %{buildroot}%{_datadir}/common-lisp/{ros/*,source/}
cd %{buildroot}%{_datadir}/common-lisp/source/std_msgs/msg
for asd in *.asd; do
  ln -s %{_datadir}/common-lisp/source/std_msgs/msg/$asd ../../../systems;
done

%post
/usr/sbin/register-common-lisp-source std_msgs

%preun
/usr/sbin/unregister-common-lisp-source std_msgs

%files
%{_datadir}/%{stackname}
%{python_sitelib}/%{stackname}
%{_datadir}/common-lisp/source/%{stackname}
%{_datadir}/common-lisp/systems/*.asd

%files devel
%{_includedir}/%{stackname}
%{_datadir}/pkgconfig/*.pc

%changelog
* Sun Jul 28 2013 Rich Mattes <richmattes@gmail.com> - 0.4.11-3.20130605gitde0dcf1
- Fix requires/provides issue in -devel package
- Require genpy and genlisp in base package
- Require roscpp_core in devel package (for c++ message headers)
- Attempt to follow the lisp packaging guidelines for lisp messages

* Thu Jul 25 2013 Rich Mattes <richmattes@gmail.com> - 0.4.11-2.20130605gitde0dcf1
- Fix BuildRequires to point to correct package names

* Wed Jun 05 2013 Rich Mattes <richmattes@gmail.com> - 0.4.11-1.20130605gitde0dcf1
- Update to 0.4.11
- Update github upstream url
- Create main package with runtime (python and lisp) msgs

* Wed Mar 27 2013 Rich Mattes <richmattes@gmail.com> - 0.4.8-2.gitef63d31
- Rename to ros-std_msgs
- Move everything to a devel subpackage

* Tue Sep 04 2012 Rich Mattes <richmattes@gmail.com> - 0.4.8-1.gitef63d31
- Initial package
