Name:           mayam
Version:        20110509
Release:        1%{?dist}
Summary:        A Cross-platform DICOM viewer developed in Java using the dcm4che toolkit

License:        MPL
URL:            http://www.dcm4che.org/confluence/display/OV/MAYAM
Source0:        %{name}-svn-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  ant
Requires:       jpackage-utils
Requires:       java

#Requires:       

%description
Viewer Features
-DICOM Listener for Q/R
-DICOM Send
-Local DB for storing study information
-Importing DICOM studies from local disk
-Parsing DicomDir from local disk or CD
-Query compressed studies without decompressing them
-Multiple Studies viewer using Layout,Tab view
-Export to JPEG (Study, Series, Instance level). Windowing can be applied to a single instance or series of instance while exporting
-Cine Loop & stack navigation
-Toggle for Text and Annotation Overlay
-Windowing Presets Settings (based on modality)
-Layout Settings (based on modality)
-AE Management
-DICOM Tags Viewer

Image Manipulation
-Windowing / Presets
-Invert, Flip & Rotate
-Zooming & Panning
-Annotation and Measurement Tools (Ruler, Rectangle and Elliptical)

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{name}

JAR files=""
for j in $(find -name \*.jar); do
if [ ! -L $j ] ; then
JAR files="$JAR files $j"
fi
done
if [ ! -z "$JAR files" ] ; then
echo "These JAR files should be deleted and symlinked to system JAR files: $JAR files"
exit 1
fi

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
ant

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
##cp -p [build path to jar] $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
##cp -rp [javadoc directory] $RPM_BUILD_ROOT%{_javadocdir}/%{name}


%files
%doc

%files javadoc


%changelog
* Mon May 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110509-1
- initial build
