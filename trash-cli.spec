%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %global pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Summary:        Command line interface to the freedesktop.org trashcan
Name:           trash-cli
Version:        0.12.4.24
Release:        1%{?dist}
License:        GPLv2+
Group:          System Environment/Base
URL  :          http://trash-cli.googlecode.com/
Source0:        http://pypi.python.org/packages/source/t/trash-cli/trash-cli-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-setuptools-devel dos2unix
Requires:       python-unipath python-setuptools

%description
trash-cli provides a command line trash usable with GNOME, KDE, Xfce or any 
freedesktop.org compatible trash implementation. The command line interface is
compatible with rm and you can use trash-put as an alias to rm.  

%prep
%setup -q 

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT 

# remove the testing part
rm -fvr $RPM_BUILD_ROOT/%{python_sitelib}/unit_tests
rm -fvr $RPM_BUILD_ROOT/%{python_sitelib}/integration_tests 

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc README.txt

%{_bindir}/trash*
%{_bindir}/restore-trash
%{python_sitelib}/trashcli/
%{python_sitelib}/trash_cli-*-py%{pyver}.egg-info
%{_mandir}/man1/trash-*
%{_mandir}/man1/restore-trash*

%changelog
* Wed Apr 25 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.12.4.24-1
- Update to new release
- update source url

* Fri Jan 06 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.11.3-0.5.r315
- spec bump for gcc 4.7 rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.3-0.4.r315
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.11.3-0.3.r315
- Updated patch

* Sun Feb 06 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.11.3-0.2.r315
- Add requires to python-setuptools
- Patch to correct trash-empty

* Tue Jan 04 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.11.3-0.1.r315 
- update to latest up stream release
- http://pypi.python.org/pypi/trash-cli/
- rename restore-trash to trash-restore : refer comment

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Feb 18 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.11.2-2
- Update as per review

* Fri Oct 23 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.11.2-1
- new upstream release
- cleaned up spec

* Mon Jun 29 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.11.1.2-1
- Updated spec for review

* Sat Mar 14 2009 Terje Rosten <terje.rosten@ntnu.no> - 0.11.0-1.r199
- initial build


