# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
%if 0%{?fedora} < 30
%global with_py2 1
%else
%global with_py2 0
%endif

%global srcname PsychoPy
%global lower_name psychopy

%global desc \
PsychoPy uses OpenGL and Python to create a toolkit for running \
psychology/neuroscience/psychophysics experiments.



Name:           python-%{lower_name}
Version:        1.90.3
Release:        1%{?dist}
Summary:        Psychology experiment software in Python


License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %pypi_source %{srcname} %{version} zip

BuildArch:      noarch
BuildRequires:  python3-devel

# From setup.py
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist pandas}
BuildRequires:  %{py3_dist pillow}
BuildRequires:  %{py3_dist wxPython}
BuildRequires:  %{py3_dist pyglet}
BuildRequires:  %{py3_dist pygame}
BuildRequires:  %{py3_dist configobj}
BuildRequires:  %{py3_dist pyopengl}
BuildRequires:  %{py3_dist cffi}
BuildRequires:  %{py3_dist xlrd}
BuildRequires:  %{py3_dist openpyxl}
BuildRequires:  %{py3_dist pyserial}
BuildRequires:  %{py3_dist pyyaml}
BuildRequires:  %{py3_dist gevent}
BuildRequires:  %{py3_dist msgpack-python}
BuildRequires:  %{py3_dist psutil}
BuildRequires:  %{py3_dist tables}
BuildRequires:  %{py3_dist zmq}
BuildRequires:  %{py3_dist pyqt5}

BuildRequires:  %{py3_dist lxml}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist sphinx}

# Not packaged
BuildRequires:  %{py3_dist soundfile}
BuildRequires:  %{py3_dist sounddevice}
BuildRequires:  %{py3_dist python-bidi}
BuildRequires:  %{py3_dist json_tricks}
BuildRequires:  %{py3_dist pyosf}
BuildRequires:  %{py3_dist pyparallel}
BuildRequires:  %{py3_dist moviepy}

Requires:  %{py3_dist numpy}
Requires:  %{py3_dist scipy}
Requires:  %{py3_dist matplotlib}
Requires:  %{py3_dist pandas}
Requires:  %{py3_dist pillow}
Requires:  %{py3_dist wxPython}
Requires:  %{py3_dist pyglet}
Requires:  %{py3_dist pygame}
Requires:  %{py3_dist configobj}
Requires:  %{py3_dist pyopengl}
Requires:  %{py3_dist cffi}
Requires:  %{py3_dist xlrd}
Requires:  %{py3_dist openpyxl}
Requires:  %{py3_dist pyserial}
Requires:  %{py3_dist pyyaml}
Requires:  %{py3_dist gevent}
Requires:  %{py3_dist msgpack-python}
Requires:  %{py3_dist psutil}
Requires:  %{py3_dist tables}
Requires:  %{py3_dist zmq}
Requires:  %{py3_dist pyqt5}

# Not packaged
Requires:  %{py3_dist soundfile}
Requires:  %{py3_dist sounddevice}
Requires:  %{py3_dist python-bidi}
Requires:  %{py3_dist json_tricks}
Requires:  %{py3_dist pyosf}
Requires:  %{py3_dist pyparallel}
Requires:  %{py3_dist moviepy}

%description
%{desc}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel 
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist scipy}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist pandas}
BuildRequires:  %{py2_dist pillow}
BuildRequires:  %{py2_dist wxPython}
BuildRequires:  %{py2_dist pyglet}
BuildRequires:  %{py2_dist pygame}
BuildRequires:  %{py2_dist configobj}
BuildRequires:  %{py2_dist pyopengl}
BuildRequires:  %{py2_dist cffi}
BuildRequires:  %{py2_dist xlrd}
BuildRequires:  %{py2_dist openpyxl}
BuildRequires:  %{py2_dist pyserial}
BuildRequires:  %{py2_dist pyyaml}
BuildRequires:  %{py2_dist gevent}
BuildRequires:  %{py2_dist msgpack-python}
BuildRequires:  %{py2_dist psutil}
BuildRequires:  %{py2_dist tables}
BuildRequires:  %{py2_dist zmq}
BuildRequires:  %{py2_dist pyqt5}

BuildRequires:  %{py2_dist lxml}
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist sphinx}

# Not packaged
BuildRequires:  %{py2_dist soundfile}
BuildRequires:  %{py2_dist sounddevice}
BuildRequires:  %{py2_dist python-bidi}
BuildRequires:  %{py2_dist json_tricks}
BuildRequires:  %{py2_dist pyosf}
BuildRequires:  %{py2_dist pyparallel}
BuildRequires:  %{py2_dist moviepy}

Requires:  %{py2_dist numpy}
Requires:  %{py2_dist scipy}
Requires:  %{py2_dist matplotlib}
Requires:  %{py2_dist pandas}
Requires:  %{py2_dist pillow}
Requires:  %{py2_dist wxPython}
Requires:  %{py2_dist pyglet}
Requires:  %{py2_dist pygame}
Requires:  %{py2_dist configobj}
Requires:  %{py2_dist pyopengl}
Requires:  %{py2_dist cffi}
Requires:  %{py2_dist xlrd}
Requires:  %{py2_dist openpyxl}
Requires:  %{py2_dist pyserial}
Requires:  %{py2_dist pyyaml}
Requires:  %{py2_dist gevent}
Requires:  %{py2_dist msgpack-python}
Requires:  %{py2_dist psutil}
Requires:  %{py2_dist tables}
Requires:  %{py2_dist zmq}
Requires:  %{py2_dist pyqt5}

# Not packaged
Requires:  %{py2_dist soundfile}
Requires:  %{py2_dist sounddevice}
Requires:  %{py2_dist python-bidi}
Requires:  %{py2_dist json_tricks}
Requires:  %{py2_dist pyosf}
Requires:  %{py2_dist pyparallel}
Requires:  %{py2_dist moviepy}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}


%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%if %{with_py2}
%py2_build
%endif

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
# If, however, we're installing separate executables for python2 and python3,
# the order needs to be reversed so the unversioned executable is the python2 one.
%if %{with_py2}
%py2_install
%endif

%py3_install

%check
%if %{with_py2}
%{__python2} setup.py test
%endif
%{__python3} setup.py test

%if %{with_py2}
%files -n python2-%{srcname}
%license COPYING
%doc README.rst
# update this, wild cards are now forbidden
%{python2_sitelib}/*
%endif

%files -n python3-%{srcname}
%license COPYING
%doc README.rst
# update this, wild cards are now forbidden
# %{python3_sitelib}/*
# %{_bindir}/sample-exec

%changelog
* Sat Nov 03 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.2.3-1
- Initial build
