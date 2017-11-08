%global module  brian2

Name:           python-%{module}
Version:        2.0b4
Release:        0.1%{?dist}
Summary:        A clock driven simulator for spiking neural networks

License:        CeCILL
URL:            http://briansimulator.org/

Source0:        https://pypi.python.org/packages/source/B/Brian2/Brian2-%{version}.tar.bz2
Source1:        https://raw.githubusercontent.com/brian-team/brian2/master/LICENSE

BuildRequires:  python2-devel numpy numpy-f2py python-sphinx sympy pyparsing
BuildRequires:  python-sphinxcontrib-issuetracker Cython

BuildRequires:  python3-devel python3-numpy python3-numpy-f2py python3-sphinx
BuildRequires:  python3-sympy python3-pyparsing
BuildRequires:  python3-sphinxcontrib-issuetracker python3-Cython

#Note-- docs not built because they need to retrieve artefacts from the
#internet
BuildRequires:  python-nose
BuildRequires:  python3-nose

%description
Brian is a simulator for spiking neural networks available on almost all
platforms.  The motivation for this project is that a simulator should not only
save the time of processors, but also the time of scientists.

It is the successor of Brian1 and shares its approach of being highly flexible
and easily extensible. It is based on a code generation framework that allows
to execute simulations using other programming languages and/or on different
devices.

This software is considered  to be in the beta status, please report
issues to the GitHub issue tracker
(https://github.com/brian-team/brian2/issues) or to the brian-development
mailing list (http://groups.google.com/group/brian-development/)

Documentation for Brian2 can be found online at http://brian2.readthedocs.org

%package -n python2-%{module}
Summary:        A clock driven simulator for spiking neural networks
Requires:       scipy numpy python-matplotlib sympy numpy-f2py
%{?python_provide:%python_provide python2-%{module}}

%description -n python2-%{module}
Brian is a simulator for spiking neural networks available on almost all
platforms.  The motivation for this project is that a simulator should not only
save the time of processors, but also the time of scientists.

It is the successor of Brian1 and shares its approach of being highly flexible
and easily extensible. It is based on a code generation framework that allows
to execute simulations using other programming languages and/or on different
devices.

This software is considered  to be in the beta status, please report
issues to the GitHub issue tracker
(https://github.com/brian-team/brian2/issues) or to the brian-development
mailing list (http://groups.google.com/group/brian-development/)

Documentation for Brian2 can be found at http://brian2.readthedocs.org

%package -n python3-%{module}
Summary:        A clock driven simulator for spiking neural networks
Requires:       python3-scipy python3-numpy python3-matplotlib python3-sympy
Requires:       python3-numpy-f2py
%{?python_provide:%python_provide python3-%{module}}

%description -n python3-%{module}
Brian is a simulator for spiking neural networks available on almost all
platforms.  The motivation for this project is that a simulator should not only
save the time of processors, but also the time of scientists.

It is the successor of Brian1 and shares its approach of being highly flexible
and easily extensible. It is based on a code generation framework that allows
to execute simulations using other programming languages and/or on different
devices.

This software is considered  to be in the beta status, please report
issues to the GitHub issue tracker
(https://github.com/brian-team/brian2/issues) or to the brian-development
mailing list (http://groups.google.com/group/brian-development/)

Documentation for Brian2 can be found at http://brian2.readthedocs.org

%package examples
Summary:    Examples for %{name}
BuildArch:  noarch

%description examples
This package contains examples for %{name}.

%prep
%setup -q -n Brian2-%{version}

cp %{SOURCE1} .
rm -rf Brian2.egg-info

#examples shouldn't be exectuable
find examples/ -name "*.py" -exec chmod -x '{}' \;

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

# Need brian1 or something apparently?
#%check
#%{__python2} setup.py check --strict
#%{__python2} setup.py nosetests
#%{__python3} setup.py check --strict
#%{__python3} setup.py nosetests

%files -n python2-%{module}
%doc README.rst
%license LICENSE
%{python2_sitearch}/%{module}/
%{python2_sitearch}/Brian2-%{version}-py?.?.egg-info

%files -n python3-%{module}
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{module}/
%{python3_sitearch}/Brian2-%{version}-py?.?.egg-info

%files examples
%doc examples

%changelog
* Wed Aug 05 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 2.0b4-0.1
- Initial build

* Tue Apr 21 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 2.0b2-0.1
- Brian2 is here

* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.4.1-1
- Split docs to separate subpackage
- Remove stray changelog entry
- No hardcoded macros used - not sure what fedora-review found
- All source files rarely contain a license header - the license is clear
- unversioned shared objects are in private libdir
- egg info is provided
- mailed upstream to include a license file

* Sun May 18 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.4.1-1
- Initial rpm build
