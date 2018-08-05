%global srcname neurosynth

%global desc \
Neurosynth is a Python package for large-scale synthesis of functional \
neuroimaging data.

Name:           python-%{srcname}
Version:        0.3.7
Release:        1%{?dist}
Summary:        Large-scale synthesis of functional neuroimaging data

License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %pypi_source

BuildArch:      noarch
BuildRequires:  python2-devel python3-devel

%description
%{desc}

%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist nibabel}
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist scipy}
BuildRequires:  %{py2_dist pandas}
BuildRequires:  %{py2_dist ply}
BuildRequires:  %{py2_dist six}
BuildRequires:  %{py2_dist scikit-learn}
BuildRequires:  %{py2_dist biopython}
Requires:  %{py2_dist matplotlib}
Requires:  %{py2_dist nibabel}
Requires:  %{py2_dist numpy}
Requires:  %{py2_dist scipy}
Requires:  %{py2_dist pandas}
Requires:  %{py2_dist ply}
Requires:  %{py2_dist six}
Requires:  %{py2_dist scikit-learn}
Requires:  %{py2_dist biopython}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist nibabel}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist pandas}
BuildRequires:  %{py3_dist ply}
BuildRequires:  %{py3_dist six}
BuildRequires:  %{py3_dist scikit-learn}
BuildRequires:  %{py3_dist biopython}
Requires:  %{py3_dist matplotlib}
Requires:  %{py3_dist nibabel}
Requires:  %{py3_dist numpy}
Requires:  %{py3_dist scipy}
Requires:  %{py3_dist pandas}
Requires:  %{py3_dist ply}
Requires:  %{py3_dist six}
Requires:  %{py3_dist scikit-learn}
Requires:  %{py3_dist biopython}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}


%prep
%autosetup -n %{srcname}-%{version}
rm -fr neurosynth.egg-info

%build
%py2_build
%py3_build

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
# If, however, we're installing separate executables for python2 and python3,
# the order needs to be reversed so the unversioned executable is the python2 one.
%py2_install
%py3_install

%check
%{__python2} setup.py test
%{__python3} setup.py test

# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files -n python2-%{srcname}
%license LICENSE
%doc README.md
%{python2_sitelib}/*

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*
%{_bindir}/sample-exec

%changelog
* Sun Aug 05 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.7-1
- Initial incomplete rpmbuild
- depends on broken nibabel
