%global module_name genlisp
%{?scl:%scl_package genlisp}
%{!?scl:%global pkg_name %{name}}

# Python globals
%global pybasever 2.7
%global pylibdir %{_libdir}/python%{pybasever}
%global scl_python_sitearch %{pylibdir}/site-packages
%global scl_python_sitelib %{_prefix}/lib/python%{pybasever}/site-packages


Name:           %{?scl_prefix}%{module_name}
Version:        0.4.10
Release:        1%{?dist}
Summary:        ROS groovy %{module_name} module
BuildArch:      noarch

License:        BSD
URL:            http://www.ros.org/wiki/roslisp

# wget --content-disposition https://github.com/ros/genlisp/archive/0.4.10.tar.gz
Source0:        %{module_name}-%{version}.tar.gz

# BuildRequires
BuildRequires:       ros-groovy-catkin-devel
BuildRequires:       ros-groovy-genmsg-devel



# Requires
Requires:        ros-groovy-genmsg


%{?scl:Requires: %scl_runtime}

%description
Common-Lisp ROS message and service generators.

%package devel
Summary: Development files for %{name}
Requires:  %{?scl_prefix}%{module_name} = %{version}-%{release}

%description devel
Development files for %{module_name}


%prep
%setup -q -n %{module_name}-%{version}


%build

# Remove the scl enabling if it isn't required. Generally required to build packages on top of catkin
# They're all conditionals and will not be run if scl isn't defined.
%{?scl:scl -l}

%{?scl:scl enable %{scl} - << \EOF}
python -c 'import sys; print sys.path'

mkdir build
pushd build
    %cmake  .. -DCATKIN_BUILD_BINARY_PACKAGE="1" -DSETUPTOOLS_DEB_LAYOUT=OFF -Dgenmsg_DIR=%{_datadir}/genmsg/cmake/
    make %{?_smp_mflags}
popd
#pushd doc
#   export PYTHONPATH=$(pwd)/src/genmsg
#    make html man
#popd
%{?scl:EOF}

%install
%{?scl:scl -l}
%{?scl:scl enable %{scl} "}
make -C build install DESTDIR=$RPM_BUILD_ROOT
%{?scl:"}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ros-langs/
mv -v $RPM_BUILD_ROOT/%{?_scl_root}/%{_usr}/etc/ros/genmsg/%{module_name} $RPM_BUILD_ROOT%{_sysconfdir}/ros-langs/

# Move packageconfig to correct location
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig
mv -v $RPM_BUILD_ROOT/%{?_scl_root}/%{_usr}/lib/pkgconfig/%{module_name}.pc $RPM_BUILD_ROOT/%{_datadir}/pkgconfig

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mv -v $RPM_BUILD_ROOT%{?_scl_root}/%{_usr}/lib/%{module_name}/gen_lisp.py $RPM_BUILD_ROOT%{_bindir}

%check 
#%{?scl:scl -l}
#%{?scl:scl enable %{scl} "}
#%{?scl:export PYTHONPATH=$PYTHONPATH:%{?scl_python_sitelib}:%{?scl_python_sitearch}}

# OR ANOTHER COMMAND
#python setup.py test 
#%{?scl:"}

%files
%{scl_python_sitelib}/*
%dir %{_datadir}/%{module_name}
%{_datadir}/%{module_name}/package.xml
%{_datadir}/%{module_name}/*.template
%config(noreplace)%{_sysconfdir}/ros-langs/*
%{_bindir}/gen_lisp.py

%files devel
%{_datadir}/%{module_name}/cmake
%{_datadir}/pkgconfig/*.pc


%changelog
# Need to replace it with today's date
* Sun Aug 04 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.10 -1
- Initial rpm build

