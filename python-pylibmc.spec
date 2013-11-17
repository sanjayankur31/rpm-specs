%global git_date    20110805
%global git_version f01c31

Name:           python-pylibmc
Version:        1.2.0
Release:        3.%{git_date}git%{git_version}%{?dist}
Summary:        Memcached client for Python

Group:          Development/Libraries
License:        BSD
URL:            http://sendapatch.se/projects/pylibmc/

# git clone https://github.com/lericson/pylibmc
# cd pylibmc
# git archive --format=tar HEAD | xz  > {name}-{version}.{git_date}git{git_version}.tar.xz
Source0:        %{name}-%{version}.%{git_date}git%{git_version}.tar.xz      

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  libmemcached-devel
BuildRequires:  zlib-devel

%description
pylibmc is a client in Python for memcached. It is a wrapper
around TangentOrg‘s libmemcached library. The interface is 
intentionally made as close to python-memcached as possible, 
so that applications can drop-in replace it.

%prep
%setup -q -cn %{name}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
chmod 755 $RPM_BUILD_ROOT%{python_sitearch}/_pylibmc.so
 
%files
%doc docs/ LICENSE README.rst TODO
%{python_sitearch}/*.egg-info/
%{python_sitearch}/pylibmc/
%{python_sitearch}/*.so


%changelog
* Tue Aug 09 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.2.0-3.20110805gitf01c31
- Changed file pylibmc.so permission

* Tue Aug 09 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.2.0-2.20110805gitf01c31
- Added soname files

* Fri Aug 05 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.2.0-1.20110805gitf01c31
- Initial RPM release
