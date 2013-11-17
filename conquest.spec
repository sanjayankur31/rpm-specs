Name:           conquest
Version:        1.4.16
Release:        1%{?dist}
Summary:        A full featured DICOM server

License:        GPLv2+
URL:            http://ingenium.home.xs4all.nl/dicom.html
Source0:        %{name}linux1416.tar.gz
Source1:        Makefile.conquest

BuildRequires:  jasper-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  lua-devel



%description
Some possible applications of the Conquest DICOM software are:

- DICOM training and testing
- Demonstration and research image archives
- Image format conversion from a scanner with DICOM network access
- DICOM image viewing and slide making
- DICOM image selection, (limited) editing, and splitting and 
merging of series
- Advanced scriptable image modification, filtering, forwarding 
and conversion
- DICOM caching and archive merging
- DICOM web access for viewing and data management (scriptable) 

%package mysql
BuildRequires:  mysql-devel
Summary:    %{name} built for mysql

%description mysql
This package contains the dgate binary built with mysql support.


%package sqlite
Summary:    %{name} built for sqlite

%description sqlite
This package contains the dgate binary built with sqlite support.


%package postgresql
BuildRequires:  postgresql-devel
Summary:    %{name} built for postgresql

%description postgresql
This package contains the dgate binary built with postgresql support.


%prep
%setup -q -c %{name}
# Remove bundled sources
rm -rf lua_5.1.4 jpeg-6c jasper-1.900.1-6ct
cp -v %{SOURCE1} ./Makefile


%build
export CFLAGS="%{optflags}"
make %{?_smp_mflags}



%install
# Install manually


%files
%doc



%changelog
* Thu Aug 11 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.16-1
- Initial rpmbuild
