%global module  brian

Name:           python-%{module}
Version:        1.4.1
Release:        1%{?dist}
Summary:        A simulator for spiking neural networks

License:        CeCILL
URL:            http://briansimulator.org/

# http://neuralensemble.org/trac/brian/downloader/download/release/19/1.4.1
Source0:        %{module}-%{version}.tar.gz
# docs, examples, tutorials
Source1:        %{module}-%{version}-extras.zip

BuildRequires:  python2-devel numpy
Requires:       scipy numpy python-matplotlib sympy

%description
Brian is a simulator for spiking neural networks available on almost all
platforms.  The motivation for this project is that a simulator should not only
save the time of processors, but also the time of scientists.

Brian is easy to learn and use, highly flexible and easily extensible. The
Brian package itself and simulations using it are all written in the Python
programming language, which is an easy, concise and highly developed language
with many advanced features and development tools, excellent documentation and
a large community of users providing support and extension packages.


%package docs
Summary:    Documentation for %{name}
BuildArch:  noarch

%description docs
This package contains examples, tutorials and documentation for %{name}.

%prep
%setup -q -n %{module}-%{version}

# Manually unzip extras
cp %{SOURCE1} .
unzip %{module}-%{version}-extras.zip

find . -name "*.*" -exec sed -i 's/\r$//' '{}' \;

find docs -name "*.py" -exec chmod -v 0644 '{}' \;
find examples -name "*.py" -exec chmod -v 0644 '{}' \;
find tutorials -name "*.py" -exec chmod -v 0644 '{}' \;

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

chmod 0755 $RPM_BUILD_ROOT/%{python2_sitearch}/%{module}/utils/ccircular/_ccircular.so
chmod 0755 $RPM_BUILD_ROOT/%{python2_sitearch}/%{module}/utils/fastexp/_fastexp.so

for lib in $RPM_BUILD_ROOT%{python2_sitearch}/%{module}/{experimental/cspikequeue,utils/{fastexp,ccircular}}/setup.py;
do
 sed -e '1{\@^#!/usr/bin/env python@d}' -e '1{\@^#! /usr/bin/env python@d}'  $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done


%check
%{__python2} setup.py check --strict

%files
%doc README.txt 
%{python2_sitearch}/%{module}*.py*
%{python2_sitearch}/%{module}/
%{python2_sitearch}/%{module}-%{version}-py?.?.egg-info

%files docs
%doc docs examples tutorials

%changelog
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
