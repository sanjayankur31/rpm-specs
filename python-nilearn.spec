# Requires nibabel that is py3 only in Fedora
%global with_py2 0

%global srcname nilearn

%global desc %{expand: \
Nilearn is a Python module for fast and easy statistical learning on
NeuroImaging data.

It leverages the scikit-learn Python toolbox for multivariate statistics with
applications such as predictive modelling, classification, decoding, or
connectivity analysis.

This work is made available by a community of people, amongst which the INRIA
Parietal Project Team and the scikit-learn folks, in particular P. Gervais, A.
Abraham, V. Michel, A. Gramfort, G. Varoquaux, F. Pedregosa, B. Thirion, M.
Eickenberg, C. F. Gorgolewski, D. Bzdok, L. Esteve and B. Cipollini.

Detailed documentation is available at http://nilearn.github.io/.}

Name:           python-%{srcname}
Version:        0.4.2
Release:        2%{?dist}
Summary:        Python module for fast and easy statistical learning on NeuroImaging data

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %pypi_source

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist scikit-learn}
BuildRequires:  %{py3_dist joblib}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist nibabel}
BuildRequires:  %{py3_dist sphinx}
Requires:  %{py3_dist numpy}
Requires:  %{py3_dist scipy}
Requires:  %{py3_dist scikit-learn}
Requires:  %{py3_dist joblib}
Requires:  %{py3_dist nibabel}
Recommends:  %{py3_dist matplotlib}

%description
%{desc}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist scipy}
BuildRequires:  %{py2_dist scikit-learn}
BuildRequires:  %{py2_dist joblib}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist nose}
BuildRequires:  %{py2_dist nibabel}
Requires:  %{py2_dist numpy}
Requires:  %{py2_dist scipy}
Requires:  %{py2_dist scikit-learn}
Requires:  %{py2_dist joblib}
Requires:  %{py2_dist nibabel}
Recommends:  %{py2_dist matplotlib}
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
# Remove shebangs
find . -name "*py" -exec sed -i '/#!\/usr\/bin\/env python/ d' '{}' \;
# Remove pre-compiled files
find . -name "*pyc" -exec rm -f '{}' \;

%build
%py3_build

%if %{with_py2}
%py2_build
%endif

# Documentation also fetches imaging data set from online sources, so we cannot
# generate it. We include the link to the documentation in the description.

%install
%if %{with_py2}
%py2_install
%endif

%py3_install

%check
# Tests fetch data sets from online sources, and therefore cannot be run.

%if %{with_py2}
%files -n python2-%{srcname}
%license LICENSE
%doc AUTHORS.rst README.rst
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py2.?.egg-info
%endif

%files -n python3-%{srcname}
%license LICENSE
%doc AUTHORS.rst README.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py3.?.egg-info

%changelog
* Fri Nov 09 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.2-2
- Correct license
- Remvoe shebangs
- Remove pre-compiled files

* Thu Nov 08 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.2-1
- Initial build
