# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# http://rpm.org/user_doc/conditional_builds.html
%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2
%endif

# Enabled by default
%bcond_with tests

%global pypi_name spyking-circus
%global python_name spyking_circus

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
Source0:        https://github.com/%{pypi_name}/%{pypi_name}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  gcc

%{?python_enable_dependency_generator}

%description
%{desc}

%if %{with py2}
%package -n python2-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist setuptools}
BuildRequires:  %{py2_dist mpi4py}
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist Cython}
BuildRequires:  %{py2_dist scipy}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist h5py}
BuildRequires:  %{py2_dist colorama}
BuildRequires:  %{py2_dist psutil}
BuildRequires:  %{py2_dist tqdm}
BuildRequires:  %{py2_dist blosc}
BuildRequires:  %{py2_dist scikit-learn}
BuildRequires:  python2-qt5
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{desc}
%endif

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist mpi4py}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist Cython}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist h5py}
BuildRequires:  %{py3_dist colorama}
BuildRequires:  %{py3_dist psutil}
BuildRequires:  %{py3_dist tqdm}
BuildRequires:  %{py3_dist blosc}
BuildRequires:  %{py3_dist scikit-learn}
BuildRequires:  python3-qt5

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

pushd docs_sphinx
    make SPHINXBUILD=sphinx-build-3 html
popd
rm -rf docs/.doctrees
rm -rf docs/.buildinfo

%install
%if %{with py2}
%py2_install
rm -f $RPM_BUILD_ROOT/%{_bindir}/circus*
rm -f $RPM_BUILD_ROOT/%{_bindir}/spyking*
rm -rf $RPM_BUILD_ROOT/%{pypi_name}/
%endif

%py3_install
# Manually install probe files
install -p -m 0644 -d $RPM_BUILD_ROOT/%{_datadir}/
mv -v $RPM_BUILD_ROOT/%{pypi_name} $RPM_BUILD_ROOT/%{_datadir}/

%check
%if %{with tests}
%if %{with py2}
%{__python2} setup.py test
%endif
%{__python3} setup.py test
%endif

%if %{with py2}
%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst AUTHORS changelog
%{python2_sitelib}/%{python_name}-%{version}-py2.?.egg-info
%{python2_sitelib}/circus
%{_datadir}/%{pypi_name}
%endif

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst AUTHORS changelog
%{python3_sitelib}/%{python_name}-%{version}-py3.?.egg-info
%{python3_sitelib}/circus
%{_datadir}/%{pypi_name}
%{_bindir}/circus-artefacts
%{_bindir}/circus-folders
%{_bindir}/circus-gui-matlab
%{_bindir}/circus-gui-python
%{_bindir}/circus-multi
%{_bindir}/spyking-circus
%{_bindir}/spyking-circus-launcher
%{_bindir}/spyking-circus-subtask

%files doc
%license LICENSE
%doc docs/html

%changelog
* Wed Nov 28 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.7.4-1
- Initial build
