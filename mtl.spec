Name:           mtl
Version:        4.0.9082
Release:        1%{?dist}
Summary:        The matrix template library - open source edition

License:        MTL4
URL:            http://www.simunova.com/%{name}4
Source0:        http://www.simunova.com/downloads/%{name}4/MTL-all-%{version}-Linux.tar.gz

# Explicit needed?
BuildArch:      noarch

%description
The Matrix Template Library 4 incorporates the most modern 
programming techniques to provide an easy and intuitive 
interface to users while enabling optimal performance. The 
natural mathematical notation in MTL4 empowers all engineers 
and scientists to implement their algorithms and models in 
minimal time. All technical aspects are encapsulated in the 
library. This has two fundamental advantages:

* Not worrying about technical details speeds up scientific 
and engineering software development tremendously.
* Not hard-wiring hardware features in application allows for 
easy porting to new platforms. 

Features:
Open-Source Edition:

* Easy, native application interface (API)
* Intuitive mathematical notation
* Expression Templates
* Rich Expression Templates
* Meta-Tuning
* Newest Krylov-subspace methods
* Fast and memory efficient matrix assembly
* Transparent BLAS-Support (partially, complete support in separated edition)
* Transparent UMFPACK Support
* Generic Implementation
* Support GNU-Multiprecision library, Boost.Interval, Boost.Quaternion
* Nested Container (e.g. matrices of vectors) operationally differentiated
* Advanced Morton order matrix formats

%package devel
Provides:   %{name} = %{version}-%{release}
Summary:    The matrix template library - open source edition

%description devel
The Matrix Template Library 4 incorporates the most modern 
programming techniques to provide an easy and intuitive 
interface to users while enabling optimal performance. The 
natural mathematical notation in MTL4 empowers all engineers 
and scientists to implement their algorithms and models in 
minimal time. All technical aspects are encapsulated in the 
library. This has two fundamental advantages:

* Not worrying about technical details speeds up scientific 
and engineering software development tremendously.
* Not hard-wiring hardware features in application allows for 
easy porting to new platforms. 

Features:
Open-Source Edition:

* Easy, native application interface (API)
* Intuitive mathematical notation
* Expression Templates
* Rich Expression Templates
* Meta-Tuning
* Newest Krylov-subspace methods
* Fast and memory efficient matrix assembly
* Transparent BLAS-Support (partially, complete support in separated edition)
* Transparent UMFPACK Support
* Generic Implementation
* Support GNU-Multiprecision library, Boost.Interval, Boost.Quaternion
* Nested Container (e.g. matrices of vectors) operationally differentiated
* Advanced Morton order matrix formats


%package docs
Requires:   %{name} = %{version}-%{release}
Summary:    Documentation for %{name}
%description docs
%{summary}


%prep
%setup -q -n MTL-all-%{version}-Linux

# Unneeded files
rm -frv ./usr/share/%{name}/tools/

cd ./usr/share/%{name}/
tar -xvf documentation.tar.gz

rm -fv documentation.tar.gz

mv license.mtl.txt ../../../ -v
mv README ../../../ -v

cd ../../../


%build
#Nothing to do here

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p  $RPM_BUILD_ROOT/%{_includedir}/boost/numeric/
cp -vr ./usr/include/boost/numeric/mtl $RPM_BUILD_ROOT/%{_includedir}/boost/numeric/
cp -vr ./usr/include/boost/numeric/meta_math $RPM_BUILD_ROOT/%{_includedir}/boost/numeric/

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/
cp -vr ./usr/share/mtl/doc $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}
cp -vr ./usr/share/mtl/examples $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}

%files devel
%doc README license.mtl.txt
## %{_includedir}/boost/numeric/itl
## %{_includedir}/boost/numeric/linear_algebra
%{_includedir}/boost/numeric/mtl
%{_includedir}/boost/numeric/meta_math

%files docs
%{_docdir}/%{name}-%{version}


%changelog
* Tue Jan 08 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.0.9082-1
- Init://fedoraproject.org/wiki/Ambassadors/APAC/Budget/Indiatial rpm build
- Skipped tests

