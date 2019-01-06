# Not yet py3
# https://github.com/LTS5/cfflib/pull/8
%global srcname cfflib

%global desc %{expand: \
The Connectome File Format library supports handling of multi-modal
neuroimaging datasets and metadata.
}

Name:           python-%{srcname}
Version:        2.0.5
Release:        1%{?dist}
Summary:        Connectome File Format Library

License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %pypi_source

BuildArch:      noarch

%description
%{desc}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  %{py3_dist nibabel}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist numpydoc}
BuildRequires:  %{py3_dist matplotlib}

# Requires:  %{py3_dist lxml}
# Requires:  %{py3_dist urllib2}
# Requires:  %{py3_dist pyxnat}
# Requires:  %{py3_dist zipfile}
# Requires:  %{py3_dist pickle}
# Requires:  %{py3_dist pygments}
# Requires:  %{py3_dist matplotlib}

%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%{?python_enable_dependency_generator}

%prep
%autosetup -n %{srcname}-%{version}
# Remove sphinxext
rm -rf doc/source/sphinxext

%build
%py3_build

pushd doc
    SPHINXBUILD=sphinx-build-3 make html
popd

%install
%py3_install

%check
nosetests-3

%files -n python3-%{srcname}
%license COPYING
%doc README.rst

%changelog
* Sun Aug 05 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.0.5-1
- Initial incomplete spec
