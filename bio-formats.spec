Name:           bio-formats
Version:        20110705
Release:        0.1git%{?dist}
Summary:        Convert proprietary microscopy data into an open standard

License:        GPL+
URL:            http://www.loci.wisc.edu/software/bio-formats
# git clone git://dev.loci.wisc.edu/bio-formats.git  bio-formats
# tar -xvzf bio-formats-20110705.tar.gz bio-formats/
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  ant ant-contrib ant-findbugs checkstyle
BuildRequires:  OSGi-bundle-ant-task testng slf4j
Requires:       jpackage-utils log4j
Requires:       java

%description
Bio-Formats is a standalone Java library for reading and writing 
life sciences image file formats. It is capable of parsing both 
pixels and metadata for a large number of formats, as well as 
writing to several formats. See the table below for a complete 
list (click the headers to sort, and format names to see all 
information). For more information on the format ratings, see the 
Supported Formats page.

Purpose :
Bio-Formats's primary purpose is to convert proprietary microscopy 
data into an open standard called the OME data model, particularly 
into the OME-TIFF file format. See the Bio-Formats statement of 
purpose for a thorough explanation and rationale.

Bio-Formats currently supports 115 formats 

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
#export CLASSPATH=$(build-classpath net.luminis.build.plugin testng slf4j/log4j-over-slf4j slf4j/api)
#export CLASSPATH=$(build-classpath net.luminis.build.plugin testng log4j)

ln -s %{_javadir}/net.luminis.build.plugin.jar jar/net.luminis.build.plugin.jar
for i in `ls %{_javadir}/slf4j/*`; 
do
    ln -s "$i" "jar/$i"
done

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
* Fri Jun 24 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> 20110624-0.1git
- initial rpm build
