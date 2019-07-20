%global pypi_name matplotlib-scalebar

%global _description %{expand:
Provides a new artist for Matplotlib to display a scale bar, aka micron bar. It
is particularly useful when displaying calibrated images plotted using
plt.imshow(…).  The artist supports customization either directly from the
ScaleBar object or from the matplotlibrc.}



Name:           python-%{pypi_name}
Version:        0.6.0
Release:        1%{?dist}
Summary:        Artist for matplotlib to display a scale bar

License:        BSD
URL:            https://pypi.org/project/%{pypi_name}
Source0:        %pypi_source

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist nose}

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' matplotlib_scalebar/test*py

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/matplotlib_scalebar-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/matplotlib_scalebar

%changelog
* Sat Jul 20 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.6.0-1
- Update URL

* Fri Jul 19 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.6.0-1
- Initial build
