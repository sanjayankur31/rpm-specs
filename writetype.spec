%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:		writetype
Version:	1.2.130
Release:	1%{?dist}
Summary:	Light word processor
Group:		Applications/Editors
License:	GPLv3+
URL:		http://writetype.bernsteinforpresident.com/
Source0:	http://bernsteinforpresident.com/programs/%{name}_%{version}.tar.gz
Patch0:		fix_writetype-excutingfile-path.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	python2-devel
BuildRequires:	python-setuptools

Requires:	PyQt4

%description
WriteType is a free  (and open source) program that helps 
younger students experience success in writing. It is designed 
especially for schools to transform technology from a barrier 
into an opportunity for success.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .fix

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
# Remove sheband
sed -i -e '/^#!\//, 1d' %{buildroot}%{python_sitelib}/%{name}/__init__.py
sed -i -e '/^#!\//, 1d' %{buildroot}%{python_sitelib}/%{name}/espeakInterface.py
sed -i -e '/^#!\//, 1d' %{buildroot}%{python_sitelib}/%{name}/listWidget.py
sed -i -e '/^#!\//, 1d' %{buildroot}%{python_sitelib}/%{name}/ttsInterface.py
sed -i -e '/^#!\//, 1d' %{buildroot}%{python_sitelib}/%{name}/festivalInterface.py
sed -i -e '/^#!\//, 1d' %{buildroot}%{python_sitelib}/%{name}/pyttsxInterface.py
sed -i -e '/^#!\//, 1d' %{buildroot}%{python_sitelib}/%{name}/main.py
# Delete zero length file
find %{buildroot}%{_datadir}/%{name} -size 0 -delete

%clean
rm -rf %{buildroot}

#%%files -f %%{name}.lang
%files
%defattr(-,root,root,-)
%doc README
%{python_sitelib}/%{name}
%{python_sitelib}/WriteType-%{version}-py2.7.egg-info
%{_bindir}/%{name}
%{_datadir}/%{name}
%attr(0644,root,root) %{_datadir}/applications/%{name}.desktop


%changelog
* Wed Apr 20 2011 Prabin Kumar Datta <prabindatta@fedoraproject.org> - 1.2.130-1
- Initial build
