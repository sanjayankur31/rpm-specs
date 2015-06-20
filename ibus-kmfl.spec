Name:           ibus-kmfl
Version:        1.0.3
Release:        1%{?dist}
Summary:        IBus input method for KMFL

License:        GPLv2+
URL:            http://kmfl.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  ibus-devel
Requires:       ibus

%description
KMFL is a keyboarding input method currently being developed under Linux which
aims to bring Tavultesoft Keyman functionality to *nix operating systems. KMFL
is being jointly developed by SIL International (http://www.sil.org) and
Tavultesoft (http://www.tavultesoft.com). It is being released under the GPL
license.

The current implementation of KMFL uses either the iBus framework
(http://code.google.com/p/ibus) or the older SCIM framework
(http://www.scim-im.org/) to handle the input method interface to X. KMFL
consists of three parts: a library which provides an engine to interpret
compiled KMFL keyboard tables, a keyboard compiler, and an input method engine
either for SCIM or iBus. Note that the library and the keyboard compiler are
independent from the input method. This design allows KMFL to use other
frameworks such as IIIMF to provide input method services to an operating
system at a later date.

KMFL aims to be source compatible with keyboards developed for Keyman 7. Binary
keyboards compiled for Keyman will not run under KMFL. You will need to use the
source keyboard or recompile it with the supplied KMFL keyboard compiler. Any
fonts contained in the Keyman binary keyboard will have to be installed
separately. KMFL is also Unicode based, and does not support legacy code pages
and encodings.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc



%changelog
* Tue Sep 16 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.0.3-1
- Initial rpmbuild

