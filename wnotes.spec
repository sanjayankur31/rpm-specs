Name:           wnotes           
Version:        1.20
Release:        1%{?dist}
Summary:        Graphical text notes for X Window System display

License:        GPLv2+
URL:            http://unixb4coffee.hubpages.com/hub/Linux-for-Users-Notes-on-Your-Desktop
Source0:        http://wnotes.googlecode.com/files/wnotes-1.20.tar.gz

BuildRequires:  libX11-devel libXpm-devel


%description
They are Post-It type notes for X Window System desktops.
They use the Xlib libraries and are self contained.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files  
%doc COPYING README AUTHORS
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Tue Oct 02 2012 Soumya Kanti Chakraborty <soumya@fedoraproject.org> - 1.20-1
- Changed the License and updated new version.

* Fri Dec 22 2011 Soumya Kanti Chakraborty <soumya@fedoraproject.org> - 1.10-1
- Initial Release
