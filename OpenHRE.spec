Name:           OpenHRE
Version:        0.0.5
Release:        1%{?dist}
Summary:        An implementation of the National Health Information Network (NHIN)

# WOAH!
License:        Apache and BSD and LGPL and GPL and MIT and libpng
URL:            http://openhre.org/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-dist.tar.gz 
BuildArch:      noarch

BuildRequires:  jpackage-utils

BuildRequires:  java-devel

BuildRequires:  ant

Requires:       jpackage-utils

Requires:       java

%description
Mission:

* to foster development, distribution and support of standard Record Locater,
Health Record Exchange and Access Control services held as Free/Open Source
Software
* to build a community to this aim
* to realize this goal via a self-sustaining business model and open
collaboration among all stakeholders 

Goal:

* To accelerate implementation of the National Health Information Network
(NHIN) by providing Health Stakeholders an affordable means toestablish the
secure and interoperable exchange of health records between existing Health
Information systems.



%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -cn %{name}-%{version}

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
ant

%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}
#cp -p [build path to jar] $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
#cp -rp [javadoc directory] $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%{_javadir}/*
%doc

%files javadoc
%{_javadocdir}/%{name}


%changelog
* Sun Aug 14 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.5-1
- Initial rpm build
