%global commit 0b30a66659d9e64de85d526a14664dbe0415c89f
%global shortcommit %(c=%{commit}; echo ${c:0:7})


Name:       ParameterSerializer
Version:    0
Release:    20171014git%{shortcommit}%{?dist}
Summary:    An open-source library for serialization and deserialization of Insight Segmentation and Registration Toolkit (ITK) classes.

License:    Apache
URL:        https://github.com/Slicer/%{name}
Source0:  https://github.com/Slicer/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz


BuildRequires:  cmake jsoncpp-devel gcc-c++

%description
Serialization is an important technique when exploring an analysis parameter
solution space and performing reproducible research.

This is a set of classes to perform serialization and deserialization of the
parameters of ITK classes, i.e., classes that inherit from itk::LightObject.
Serialization does not require code instrumentation of the target classes. The
parameters of the target class are serialized with an archiver; the only
currently implemented archiver writes and reads JSON files with the JsonCpp
library.

The project is currently used by TubeTK and the SlicerExecutionModel.

The development of this project is supported by TubeTK.

%prep
%autosetup -n %{name}-%{shortcommit}


%build
%cmake .
make %{?_smp_mflags}


%install
%make_install


%files
%doc README.md
%license LICENSE



%changelog
* Sun Jan 14 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-20171014git0b30a666
- Initial package


