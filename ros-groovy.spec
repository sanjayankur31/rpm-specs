%{!?scl:%global scl ros-groovy}
%scl_package %scl

# Python globals
%global pybasever 2.7
%global pylibdir %{_libdir}/python%{pybasever}
%global scl_python_sitearch %{pylibdir}/site-packages
%global scl_python_sitelib %{_prefix}/lib/python%{pybasever}/site-packages

Name:       %scl_name
Version:    0
Release:    0.1%{?dist}
Summary:    Package that installs %scl
#BuildArch:  noarch
License:    GPLv2+

# Packages of ros-groovy for the time being
Requires:    %{scl_prefix}catkin
Requires:    %{scl_prefix}cpp_common
Requires:    %{scl_prefix}gencpp
Requires:    %{scl_prefix}genlisp
Requires:    %{scl_prefix}genmsg
Requires:    %{scl_prefix}genpy
Requires:    %{scl_prefix}message_filters
Requires:    %{scl_prefix}message_generation
Requires:    %{scl_prefix}message_runtime
Requires:    %{scl_prefix}mk
Requires:    %{scl_prefix}rosbag
Requires:    %{scl_prefix}rosbash
Requires:    %{scl_prefix}rosboost_cfg
Requires:    %{scl_prefix}rosbuild
Requires:    %{scl_prefix}rosclean
Requires:    %{scl_prefix}ros_comm
Requires:    %{scl_prefix}rosconsole
Requires:    %{scl_prefix}roscpp_serialization
Requires:    %{scl_prefix}roscpp
Requires:    %{scl_prefix}roscpp_traits
Requires:    %{scl_prefix}roscreate
Requires:    %{scl_prefix}rosgraph_msgs
Requires:    %{scl_prefix}rosgraph
Requires:    %{scl_prefix}roslang
Requires:    %{scl_prefix}roslaunch
Requires:    %{scl_prefix}roslib
Requires:    %{scl_prefix}roslisp
Requires:    %{scl_prefix}rosmake
Requires:    %{scl_prefix}rosmaster
Requires:    %{scl_prefix}rosmsg
Requires:    %{scl_prefix}rosnode
Requires:    %{scl_prefix}rosout
Requires:    %{scl_prefix}rospack
Requires:    %{scl_prefix}rosparam
Requires:    %{scl_prefix}rospy
Requires:    %{scl_prefix}rosservice
Requires:    %{scl_prefix}ros
Requires:    %{scl_prefix}rostest
Requires:    %{scl_prefix}rostime
Requires:    %{scl_prefix}rostopic
Requires:    %{scl_prefix}rosunit
Requires:    %{scl_prefix}roswtf
Requires:    %{scl_prefix}std_msgs
Requires:    %{scl_prefix}std_srvs
Requires:    %{scl_prefix}topic_tools
Requires:    %{scl_prefix}xmlrpcpp


BuildRequires: scl-utils-build

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%prep
%setup -c -T

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
export PYTHONPATH=\${PYTHONPATH}:%{scl_python_sitelib}:%{scl_python_sitearch}
EOF
%scl_install

%files

%files runtime
%scl_files

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Sat Feb 08 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0-0.1
- Initial build
