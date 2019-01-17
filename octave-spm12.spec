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
# It needs to be set for octave. Since we want to use the macros, I cannot pass
# this in the command as I've done above.
sed -i '29i PLATFORM = octave' src/Makefile.var

# Parallel build does not work, force make to run sequentially
echo '.NOTPARALLEL:' >> src/Makefile

make -C src distclean

# Prepare for octave pkg build
cat > DESCRIPTION <<EOF
Name: SPM12
Version: r%{revision}
Date: 2019-01-17
Author: SPM authors. See AUTHORS.txt
Maintainer: SPM authors. See README.md
Title: %{summary}
Description: %{summary}
License: GPLv2+

EOF

cp LICENCE.txt COPYING


%build
%set_build_flags
# Build mex files
make -C src
# Copy mex files to main directory
make -C src install
# Remove make files other wise `octave pkg build`
# uses them
rm -f src/Makefile*

%octave_pkg_build


%install
# Required by the octave_pkg_install macro
mkdir -p %{buildroot}/%{octpkgdir}/packinfo/
%octave_pkg_install


%post
%octave_cmd pkg rebuild

%preun
%octave_pkg_preun

%postun
%octave_cmd pkg rebuild

%files
%{octpkglibdir}
%dir %{octpkgdir}
%{octpkgdir}/*.m
%doc %{octpkgdir}/doc-cache
%{octpkgdir}/packinfo


%changelog
* Thu Jan 17 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-1.r7487
- Initial build
