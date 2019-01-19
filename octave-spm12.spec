# Issues that need resolution
# 1. License has wrong FSF address
# 2. spm_file_template.m and spm_provenance.m give parse errors.
# 3. Can external fieldtrip be used (it's bundled)

# SPM is not provided as an octave package, and upstream does not intend it to
# be used like standard octave forge packages.  Rather, it is a standalone tool
# based on Octave. So we do not install files into the standard octave
# locations. We treat it like a standard standalone application.

# Tests are matlab specific, so cannot be run.

# SPM versions are not merely upgrades, so they will be packaged as different modules
%global octpkg spm12
# Exclude .oct files from provides
%global __provides_exclude_from ^%{octpkglibdir}/.*\\.oct$

%global checkout 7487

Name:           octave-%{octpkg}
Version:        0
Release:        1.r%{checkout}%{?dist}
Summary:        Statistical Parametric Mapping
License:        GPLv2+
URL:            https://www.fil.ion.ucl.ac.uk/spm/
Source0:        https://github.com/spm/%{octpkg}/archive/r%{checkout}/%{octpkg}-r%{checkout}.tar.gz
Patch0:         0001-Add-in-built-target-to-force-serial-build.patch
Patch1:         0002-Fix-parse-errors.patch

BuildRequires:  octave-devel
BuildRequires:  git

Requires:       octave(api) = %{octave_api}
Requires(post): octave
Requires(postun): octave

# To be packaged
# https://github.com/fieldtrip/fieldtrip
Requires:     octave-fieldtrip

%description
The Octave-forge Image package provides functions for processing images. The
package also provides functions for feature extraction, image statistics,
spatial and geometric transformations, morphological operations, linear
filtering, and much more.


%prep
%autosetup -n %{octpkg}-r%{checkout} -S git
# Shape it up to be able to use octave's pkg command:

# It needs to be set for octave. Since we want to use the macros, I cannot pass
# this in the command as I've done above.
sed -i '29i PLATFORM = octave' src/Makefile.var


make -C src distclean
find . -name "*.mex*" -delete

# Prepare for octave pkg build
# Description file
cat > DESCRIPTION <<EOF
Name: SPM12
Version: %{version}
Date: 2019-01-17
Author: SPM authors. See AUTHORS.txt
Maintainer: SPM authors. See README.md
Title: %{summary}
Description: %{summary}
Categories: Neuroimaging
License: GPLv2+

EOF

# COPYING file
mv LICENCE.txt COPYING

# Copy files that should be installed to inst
mkdir inst
cp *.{m,fig,mat,txt} inst/
# Move all directories that should be installed into inst also
for afolder in "batches" "canonical" "config" "external" "@gifti" "@meeg" "rend" "spm_orthviews" "tests" "tpm" "compat" "EEGtemplates" "@file_array" "matlabbatch" "@nifti" "@slover" "toolbox" "@xmltree"; do
    cp -r "$afolder" inst/
done


%build
%set_build_flags
%octave_pkg_build


%install
%octave_pkg_install

# Remove unneeded binaries
rm %{buildroot}/%{octpkgdir}/bin/spm12-{matlab,mcr} -f

# Add link to standalone version in bindir
mkdir -p %{buildroot}%{_bindir} && pushd %{buildroot}%{_bindir} && \
ln -sv ../../%{octpkgdir}/bin/spm12-octave ./spm12-octave && \
popd

%post
%octave_cmd pkg rebuild

%preun
%octave_pkg_preun

%postun
%octave_cmd pkg rebuild

%files
%{octpkglibdir}
%dir %{octpkgdir}
# %{octpkgdir}/*.m
# %doc %{octpkgdir}/doc-cache
%doc man/manual.pdf man/ReleaseNotes.pdf help
%{octpkgdir}/packinfo
%{octpkgdir}/bin
%{_bindir}/spm12-octave


%changelog
* Thu Jan 17 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-1.r7487
- Initial build
