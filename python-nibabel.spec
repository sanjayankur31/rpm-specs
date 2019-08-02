%global modname nibabel

%global commit 3994fa5d3b14d507746ce625ac4a13ce03bac0c9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           python-%{modname}
Version:        2.5.0
Release:        0.1git%{shortcommit}%{?dist}
Summary:        Python package to access a cacophony of neuro-imaging file formats

License:        MIT and PDDL-1.0
URL:            http://nipy.org/nibabel/
Source0:        https://github.com/nipy/nibabel/archive/%{commit}/%{name}-%{shortcommit}.tar.gz 

BuildArch:      noarch

%description
Read / write access to some common neuroimaging file formats

This package provides read +/- write access to some common medical and
neuroimaging file formats, including: ANALYZE (plain, SPM99, SPM2 and
later), GIFTI, NIfTI1, NIfTI2, MINC1, MINC2, MGH and ECAT as well as Philips
PAR/REC. We can read and write Freesurfer geometry, and read Freesurfer
morphometry and annotation files. There is some very limited support for DICOM.
NiBabel is the successor of PyNIfTI.

The various image format classes give full or selective access to header (meta)
information and access to the image data is made available via NumPy arrays.

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
BuildRequires:  python3-mock
BuildRequires:  python3-six
BuildRequires:  python3-numpy
BuildRequires:  python3-scipy
BuildRequires:  python3-matplotlib
BuildRequires:  python3-pillow
BuildRequires:  python3-h5py
BuildRequires:  python3-pydicom
Requires:       python3-six
Requires:       python3-numpy
Recommends:     python3-scipy
Recommends:     python3-pydicom
# https://github.com/nipy/nibabel/issues/579
Provides:       bundled(python%{python3_version}dist(netcdf))

%description -n python3-%{modname}
Read / write access to some common neuroimaging file formats

This package provides read +/- write access to some common medical and
neuroimaging file formats, including: ANALYZE (plain, SPM99, SPM2 and
later), GIFTI, NIfTI1, NIfTI2, MINC1, MINC2, MGH and ECAT as well as Philips
PAR/REC. We can read and write Freesurfer geometry, and read Freesurfer
morphometry and annotation files. There is some very limited support for DICOM.
NiBabel is the successor of PyNIfTI.

The various image format classes give full or selective access to header (meta)
information and access to the image data is made available via NumPy arrays.

Python 3 version.

%prep
%autosetup -n %{modname}-%{commit}

# remove bundled six
rm -vrf %{modname}/externals/six.py
sed -i -e "s/nibabel.externals.six/six/" nibabel/externals/__init__.py
rm -fv nibabel/externals/tests/test_six.py

%build
%py3_build

%install
%py3_install

%check
# Fails on s390x
# https://github.com/nipy/nibabel/issues/775
nosetests-%{python3_version} -v

%files -n python3-%{modname}
%license COPYING
%{_bindir}/parrec2nii
%{_bindir}/nib-ls
%{_bindir}/nib-diff
%{_bindir}/nib-dicomfs
%{_bindir}/nib-nifti-dx
%{_bindir}/nib-tck2trk
%{_bindir}/nib-trk2tck
%{python3_sitelib}/%{modname}*
%{python3_sitelib}/nisext/

%changelog
* Fri Aug 02 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.5.0-0.1git3994fa5
- Test build for bugfix

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.4.1-1
- Update to 2.4.1

* Sat Feb 16 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.3.3-1
- Update to 2.3.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 07 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.3.1-1
- Update to latest upstream release
- Remove unneeded patch

* Mon Aug 13 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.3.0-3
- Drop python2 subpackage

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 22 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.3.0-1
- Update to 2.3.0
- No build since tests fail, issue filed: https://github.com/nipy/nibabel/issues/579

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.2.0-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 12 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.1.0-1
- Update to 2.1.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.0.2-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 23 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-1
- Update to 2.0.2
- unversioned bir to python3

* Sat Oct 31 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.1-1
- Initial package
