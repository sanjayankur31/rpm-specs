# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# http://rpm.org/user_doc/conditional_builds.html
%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2
%endif

# Enabled by default
%bcond_without tests

%global pypi_name spiking-circus

%global desc %{expand: \
SpyKING CIRCUS is a python code to allow fast spike sorting on multi channel
recordings. A publication on the algorithm can be found at
https://elifesciences.org/articles/34518

It has been tested on datasets coming from in vitro retina with 252 electrodes
MEA, from in vivo hippocampus with tetrodes, in vivo and in vitro cortex data
with 30 and up to 4225 channels, with good results. Synthetic tests on these
data show that cells firing at more than 0.5Hz can be detected, and their
spikes recovered with error rates at around 1%, even resolving overlapping
spikes and synchronous firing. It seems to be compatible with optogenetic
stimulation, based on experimental data obtained in the retina.

SpyKING CIRCUS is currently still under development. Please do not hesitate to
report issues with the issue tracker

- Documentation can be found at http://spyking-circus.rtfd.org
- A Google group can be found at http://groups.google.com/forum/#!forum/spyking-circus-users
- A bug tracker can be found at https://github.com/spyking-circus/spyking-circus/issues
- Open source ground-truth datasets used in the paper https://zenodo.org/record/1205233#.WrTFtXXwaV4
}

Name:           python-%{pypi_name}
Version:        0.7.4
Release:        1%{?dist}
Summary:        Fast and scalable spike sorting in python

License:        CeCILL
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        %pypi_source %{pypi_name}

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description
%{desc}

%if %{with py2}
%package -n python2-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python2-devel
# DELETE ME: Use standard names
BuildRequires:  %{py2_dist ...}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{desc}
%endif

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
# DELETE ME: Use standard names
BuildRequires:  %{py3_dist ...}
# For documentation
BuildRequires:  %{py3_dist sphinx}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{desc}

%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%if %{with py2}
%py2_build
%endif

pushd doc
    make SPHINXBUILD=sphinx-build-3 html
    rm -rf _build/html/.doctrees
    rm -rf _build/html/.buildinfo
popd

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
# If, however, we're installing separate executables for python2 and python3,
# the order needs to be reversed so the unversioned executable is the python2 one.
%if %{with py2}
%py2_install
%endif

%py3_install

%check
%if %{with tests}
%if %{with py2}
%{__python2} setup.py test
%endif
%{__python3} setup.py test
%endif

%if %{with py2}
%files -n python2-%{pypi_name}
%license COPYING
%doc README.rst
%{python2_sitelib}/%{pypi_name}-%{version}-py2.?.egg-info
%{python2_sitelib}/%{pypi_name}
%endif

%files -n python3-%{pypi_name}
%license COPYING
%doc README.rst
%{python3_sitelib}/%{pypi_name}-%{version}-py3.?.egg-info
%{python3_sitelib}/%{pypi_name}

%files doc
%license COPYING
%doc doc/_build/html

%changelog
