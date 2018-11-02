# Does not support python2 at all
%global srcname fslpy

%global desc \
The fslpy project is a FSL programming library written in Python. It is used by \
FSLeyes.

Name:           python-%{srcname}
Version:        1.12.0
Release:        1%{?dist}
Summary:        The FSL Python Library


License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %pypi_source

BuildArch:      noarch
BuildRequires:  python3-devel
Requires:  %{py3_dist six}
Requires:  %{py3_dist numpy}
Requires:  %{py3_dist scipy}
Requires:  %{py3_dist nibabel}
Requires:  %{py3_dist wxpython}
Requires:  %{py3_dist rtree}
# Not yet packaged
# Extra
# Requires:  %%{py3_dist trimesh}
# Requires:  %%{py3_dist indexed_gzip}

BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist pytest pytest-cov}
BuildRequires:  %{py3_dist coverage}
BuildRequires:  %{py3_dist mock}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist nibabel}
BuildRequires:  %{py3_dist deprecation}
BuildRequires:  %{py3_dist wxpython}
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  dcm2niix


%description
%{desc}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%package doc
Summary:        %{summary}

%description doc
This package contains documentation for %{name}.

%prep
%autosetup -n %{srcname}-%{version}
rm -rfv %{srcname}.egg-info

%build
%py3_build

# Build documentation
%{__python3} setup.py doc

%install
%py3_install

%check
# From https://git.fmrib.ox.ac.uk/fsl/fslpy/blob/master/.ci/test_template.sh
xvfb-run pytest-3 tests/test_idle.py
sleep 10
# Sometimes fails, sometimes passes
xvfb-run pytest-3 tests/test_platform.py

# Ignore tests that have already been done
# Ignore immv_imcp because it requires a "nobody" user
# Ignore tests that require downloading data.
# Ignore tests requiring trimesh
# Ignore test using dcm2niix
pytest-3 tests  -m "not longtest" --ignore=tests/test_idle.py --ignore=tests/test_platform.py --ignore=tests/test_immv_imcp.py --ignore=tests/test_atlases.py --ignore=tests/test_atlases_query.py --ignore=tests/test_atlasq_list_summary.py --ignore=tests/test_atlasq_ohi.py --ignore=tests/test_atlasq_query.py --ignore=tests/test_callfsl.py --ignore=tests/test_mesh.py --ignore=tests/test_dicom.py --ignore=tests/test_parse_data.py

%files -n python3-%{srcname}
%license LICENSE COPYRIGHT
%doc README.rst
%{python3_sitelib}/fsl
%{python3_sitelib}/%{srcname}-%{version}-py3.?.egg-info
%{_bindir}/atlasq
%{_bindir}/atlasquery
%{_bindir}/fsl_ents
%{_bindir}/imcp
%{_bindir}/imglob
%{_bindir}/immv

%files doc
%license LICENSE COPYRIGHT
%doc doc/html

%changelog
* Thu Nov 01 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.12.0-1
- Initial build
