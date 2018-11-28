%global desc %{expand: \
FSL is a comprehensive library of analysis tools for FMRI, MRI and DTI brain
imaging data. It runs on Apple and PCs (both Linux, and Windows via a Virtual
Machine), and is very easy to install. Most of the tools can be run both from
the command line and as GUIs ("point-and-click" graphical user interfaces). To
quote the relevant references for FSL tools you should look in the individual
tools manual pages, and also please reference one or more of the FSL overview
papers:


1. M.W. Woolrich, S. Jbabdi, B. Patenaude, M. Chappell, S. Makni, T. Behrens,
C. Beckmann, M. Jenkinson, S.M. Smith. Bayesian analysis of neuroimaging data
in FSL. NeuroImage, 45:S173-86, 2009

2. S.M. Smith, M. Jenkinson, M.W. Woolrich, C.F. Beckmann, T.E.J. Behrens, H.
Johansen-Berg, P.R. Bannister, M. De Luca, I. Drobnjak, D.E. Flitney, R. Niazy,
J. Saunders, J. Vickers, Y. Zhang, N. De Stefano, J.M. Brady, and P.M.
Matthews. Advances in functional and structural MR image analysis and
implementation as FSL. NeuroImage, 23(S1):208-19, 2004

3. M. Jenkinson, C.F. Beckmann, T.E. Behrens, M.W. Woolrich, S.M. Smith. FSL.
NeuroImage, 62:782-90, 2012
}

Name:           fsl
Version:        6.0.0
Release:        1%{?dist}
Summary:        FMRIB Software Library

# https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Licence
# Probably need to speak to legal@fp.o
License:        FSL
URL:            https://fsl.fmrib.ox.ac.uk/fsl/fslwiki
Source0:        https://fsl.fmrib.ox.ac.uk/fsldownloads/%{name}-%{version}sources.tar.gz

# In Fedora already
BuildRequires:  boost-devel
BuildRequires:  gd-devel
BuildRequires:  sqlite-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxml++-devel
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  NLopt-devel
# Version 2 or 3? (same as gtkmm)
BuildRequires:  glibmm-devel


# Not in fedora
# Most of them are old and only used by fsl, so we may bundle them.
# Ones that are still maintained, we can package separately
# https://pecl.php.net/package/GDChart
BuildRequires:  gdchart-devel
# http://www.robertnz.net/nr02doc.htm#files
BuildRequires:  newran-devel
# From cephes
# http://www.netlib.org/cephes/
BuildRequires:  cprob-devel
# https://git.fmrib.ox.ac.uk/fsl/armawrap
BuildRequires:  armawrap-devel
# http://robertnz.net/nm_intro.htm
BuildRequires:  newmat-devel
# https://math.nist.gov/iml++/
BuildRequires:  iml++-devel

%description


%prep
%autosetup


%build
%configure
%make_build


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%license add-license-file-here
%doc add-docs-here



%changelog
* Wed Nov 28 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 6.0.0-1
- Initial WIP
