# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
%if 0%{?fedora} < 30
%global with_py2 1
%else
%global with_py2 0
%endif

%global srcname brian2
%global pretty_name Brian2

%global generate_docs 0

# For the time being, while cython builds do not work:
# https://github.com/brian-team/brian2/issues/1026
%global debug_package %{nil}

%global desc %{expand: \
Brian2 is a simulator for spiking neural networks available on almost all
platforms. The motivation for this project is that a simulator should not only
save the time of processors, but also the time of scientists.

It is the successor of Brian1 and shares its approach of being highly flexible
and easily extensible. It is based on a code generation framework that allows
to execute simulations using other programming languages and/or on different
devices.

Please report issues to the github issue tracker
(https://github.com/brian-team/brian2/issues) or to the brian support mailing
list (http://groups.google.com/group/briansupport/)

Documentation for Brian2 can be found at http://brian2.readthedocs.org}

Name:           python-%{srcname}
Version:        2.2
Release:        1%{?dist}
Summary:        A clock-driven simulator for spiking neural networks


License:        CeCILL
URL:            https://pypi.python.org/pypi/%{pretty_name}
Source0:        %pypi_source %{pretty_name}
Patch0:         0001-Brian2-2.2-remove-crosscompiling.patch

BuildRequires:  python3-devel
BuildRequires:  gcc-c++ gcc

%description
%{desc}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist Cython} >= 0.18
BuildRequires:  %{py2_dist setuptools}
BuildRequires:  %{py2_dist nose}
BuildRequires:  %{py2_dist numpy} >= 1.10
BuildRequires:  %{py2_dist sympy} >= 0.7.6
BuildRequires:  %{py2_dist pyparsing}
BuildRequires:  %{py2_dist jinja2}
BuildRequires:  %{py2_dist py-cpuinfo}

Requires:       %{py2_dist numpy} >= 1.10
Requires:       %{py2_dist sympy} >= 0.7.6
Requires:       %{py2_dist pyparsing}
Requires:       %{py2_dist jinja2}
Requires:       %{py2_dist py-cpuinfo}

Suggests:       %{py2_dist ipython}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  %{py3_dist Cython} >= 0.18
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist nose}
%if %{generate_docs}
BuildRequires:  %{py3_dist sphinx}
%endif
BuildRequires:  %{py3_dist numpy} >= 1.10
BuildRequires:  %{py3_dist sympy} >= 0.7.6
BuildRequires:  %{py3_dist pyparsing}
BuildRequires:  %{py3_dist jinja2}
BuildRequires:  %{py3_dist py-cpuinfo}

Requires:       %{py3_dist numpy} >= 1.10
Requires:       %{py3_dist sympy} >= 0.7.6
Requires:       %{py3_dist pyparsing}
Requires:       %{py3_dist jinja2}
Requires:       %{py3_dist py-cpuinfo}

Suggests:       %{py3_dist ipython}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%package doc
Summary:    %{summary}
BuildArch:  noarch

%description doc
Documentation and examples for %{name}.


%prep
%autosetup -n %{pretty_name}-%{version} -p0
rm -rvf %{pretty_name}.egg-info

# Remove this since it is only an issue on Windows systems
sed -i 's|, !=4.0.0||' setup.py

%build
%py3_build

%if %{with_py2}
%py2_build
%endif

%if %{generate_docs}
# Build documentation
PYTHONPATH=.
sphinx-build-3 docs_sphinx html
%endif

%install
%if %{with_py2}
%py2_install
%endif

%py3_install

%check
%if %{with_py2}
nosetests-2
%endif
nosetests-3

%if %{with_py2}
%files -n python2-%{srcname}
%license LICENSE
%doc README.rst AUTHORS
%{python2_sitearch}/%{srcname}
%{python2_sitearch}/%{pretty_name}-%{version}-py2.?.egg-info
%endif

%files -n python3-%{srcname}
%license LICENSE
%{python3_sitearch}/%{srcname}
%{python3_sitearch}/%{pretty_name}-%{version}-py3.?.egg-info
%doc README.rst AUTHORS

%files doc
%license LICENSE
%doc examples tutorials
%if %{generate_docs}
%doc html
%endif

%changelog
* Sat Nov 10 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.2-1
- Initial build
