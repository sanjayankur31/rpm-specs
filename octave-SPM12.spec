# SPM versions are not merely upgrades, so they will be packaged as different modules
%global octpkg spm12
# Exclude .oct files from provides
%global __provides_exclude_from ^%{octpkglibdir}/.*\\.oct$

%global revision 7487

Name:           octave-%{octpkg}
Version:        0
Release:        1.r%{revision}%{?dist}
Summary:        Statistical Parametric Mapping
License:        GPLv2+
URL:            https://www.fil.ion.ucl.ac.uk/spm/
Source0:        https://github.com/spm/%{octpkg}/archive/r%{revision}/%{octpkg}-r%{revision}.tar.gz

BuildRequires:  octave-devel

Requires:       octave(api) = %{octave_api}
Requires(post): octave
Requires(postun): octave

%description
The Octave-forge Image package provides functions for processing images. The
package also provides functions for feature extraction, image statistics,
spatial and geometric transformations, morphological operations, linear
filtering, and much more.


%prep
%autosetup -n %{octpkg}-r%{revision}
make -C src distclean PLATFORM=octave


%build
%set_build_flags
make -C src PLATFORM=octave
# %%octave_pkg_build


%install
make -C src install PLATFORM=octave
# %%octave_pkg_install


%post
# %%octave_cmd pkg rebuild

%preun
# %%octave_pkg_preun

%postun
# %%octave_cmd pkg rebuild

%files
# %{octpkglibdir}
# %dir %{octpkgdir}
# %{octpkgdir}/*.m
# %doc %{octpkgdir}/doc-cache
# %{octpkgdir}/packinfo


%changelog
* Thu Jan 17 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-1.r7487
- Initial build
