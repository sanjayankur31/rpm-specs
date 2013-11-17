%global svn_release 475
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
# svn export -r 475 http://svn.musepack.net/libmpc/trunk/ libmpc_r475
# tar -cvzf libmpc_r475.tar.gz libmpc_r475/
Source0:        %{actual_name}_r%{svn_release}.tar.gz

BuildRequires:  cmake libreplaygain-devel libcuefile-devel


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
Obsoletes:      libmpcdec < 1.2.6-13

%description -n libmpcdec
Musepack audio decoding library


%package -n libmpcdec-devel
Summary:    Musepack audio decoding library
Obsoletes:      libmpcdec-devel < 1.2.6-13
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       libmpcdec%{?_isa} = %{version}-%{release}

%description -n libmpcdec-devel
The libmpcdec-devel package contains libraries and header files for
developing applications that use libmpcdec


%prep
%setup -q -n %{actual_name}_r%{svn_release}
# The headers are in the libcuefile dir, not cuetools since the musepack
# version of the libs are kind of a fork and I didn't want them to clash
sed -ibackup "s/cuetools/libcuefile/" mpcchap/CMakeLists.txt
sed -ibackup "s/cuetools/libcuefile/" mpcchap/mpcchap.c

# Some cmake configuration changes
# Remove quiet build
sed -ibackup '7d' CMakeLists.txt
# Don't let it override our standard flags
# It's like 18,20, but since I've deleted a line above, it becomes 17-19
sed -ibackup '17,19d' CMakeLists.txt


%build
%cmake -DWIN32:BOOL=OFF .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Versioning not clear. Should it be .7.0.1 as in libmpcdec/Makefile.am?
#pushd libmpcdec
#    ln -svf libmpcdec.so libmpcdec.so.0
#popd

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/
cp -v libmpcdec/libmpcdec.so* $RPM_BUILD_ROOT/%{_libdir}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/mpc2sv8
%{_bindir}/mpcchap
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
# README just has wrong information
%doc %{actual_name}dec/{AUTHORS,COPYING,ChangeLog}
#%{_libdir}/*.so.*
%{_bindir}/mpcdec

%files -n libmpcdec-devel
%{_includedir}/mpc/mpcdec.h
%{_libdir}/*.so

%changelog
* Sun Oct 13 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.0-0.1.svn475
- Initial rpm build

