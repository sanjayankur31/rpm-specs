%global svn_release 484
%global actual_name libmpc

# Since %{actual_name} refers to another package already
Name:           musepack-%{actual_name}
# From libmpcdec/
Version:        1.3.0
Release:        0.1.svn%{svn_release}%{?dist}
Summary:        Living audio compression

License:        BSD and LGPLv2+
URL:            http://www.musepack.net/
# Generated from the svn checkout
# svn export -r 484 http://svn.musepack.net/libmpc/trunk/ libmpc_r84
# tar -cvzf libmpc_r484.tar.gz libmpc_r484/
Source0:        %{actual_name}_r%{svn_release}.tar.gz

# use libcuefile
# Adapted from http://anonscm.debian.org/gitweb/?p=pkg-multimedia/libmpc.git;a=tree;f=debian/patches;h=37c53c4ec00439acdc7bb69d4396d070ba2fd28d;hb=8f921bb65eaebdd55fcd99064c193e7c94297b50
Patch0:         0001-%{actual_name}-mpcchap.patch

BuildRequires:  libreplaygain-devel libcue-devel autoconf automake libtool


%description
Musepack is an audio compression format with a strong emphasis on high quality.
It's not lossless, but it is designed for transparency, so that you won't be
able to hear differences between the original wave file and the much smaller
MPC file.

It is based on the MPEG-1 Layer-2 / MP2 algorithms, but since 1997 it has
rapidly developed and vastly improved and is now at an advanced stage in which
it contains heavily optimized and patentless code.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n libmpcdec
Summary:    Musepack audio decoding library

%description -n libmpcdec
Musepack audio decoding library


%package -n libmpcdec-devel
Summary:    Musepack audio decoding library
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       libmpcdec%{?_isa} = %{version}-%{release}

%description -n libmpcdec-devel
The libmpcdec-devel package contains libraries and header files for
developing applications that use libmpcdec


%prep
%setup -q -n %{actual_name}_r%{svn_release}
%patch0 -p1

%build
autoreconf -v -i .
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n libmpcdec -p /sbin/ldconfig
%postun -n libmpcdec -p /sbin/ldconfig

%files
%{_bindir}/mpc2sv8
%{_bindir}/mpccut
%{_bindir}/mpcenc
%{_bindir}/mpcgain
%{_bindir}/wavcmp

%files devel
%dir %{_includedir}/mpc/
%{_includedir}/mpc/datatypes.h
%{_includedir}/mpc/minimax.h
%{_includedir}/mpc/mpc_types.h
%{_includedir}/mpc/mpcmath.h
%{_includedir}/mpc/reader.h
%{_includedir}/mpc/streaminfo.h

%files -n libmpcdec
## README just has wrong information
%doc %{actual_name}dec/{AUTHORS,COPYING,ChangeLog}
%{_libdir}/*.so.*
%{_bindir}/mpcdec

%files -n libmpcdec-devel
%{_includedir}/mpc/mpcdec.h
%{_libdir}/*.so

%changelog
* Thu Jul 17 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.0-0.1.svn484
- Update to svn 484
- use autotools build system instead of cmake
- remove obsoletes
- builds with libcue now

* Sun Oct 13 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.0-0.1.svn475
- Initial rpm build

