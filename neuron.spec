Name:       neuron
Version:    7.2
Release:    1%{?dist}
Summary:    For empirically-based simulations of neurons and networks of neurons

License:    GPLv2+
URL:        http://www.neuron.yale.edu/neuron/
Source0:    http://www.neuron.yale.edu/ftp/neuron/versions/v%{version}/nrn-%{version}.tar.gz

BuildRequires:  ncurses-devel InterViews-devel readline

%description
NEURON is a simulation environment for modeling individual neurons and networks
of neurons. It provides tools for conveniently building, managing, and using
models in a way that is numerically sound and computationally efficient. It is
particularly well-suited to problems that are closely linked to experimental
data, especially those that involve cells with complex anatomical and
biophysical properties.


%prep
%setup -q -n nrn-%{version}
sed -i 's|IV_LIBDIR="$IV_DIR"/"$host_cpu"/lib|IV_LIBDIR="$RPM_BUILD_ROOT/%{_libdir}"|' configure
sed -i 's|IV_INCLUDE=-I$IV_DIR/include|IV_INCLUDE=-I$RPM_BUILD_ROOT/%{_includedir}|' configure


%build
%configure --with-iv=%{_includedir}/
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc



%changelog
* Sun Mar 17 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 7.2-1
- initial rpmbuild


