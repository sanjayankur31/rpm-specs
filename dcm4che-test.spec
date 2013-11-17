# use dcm4che-test as name, no use carrying the version in the name
%global svn_rev 15516

Name:           dcm4che-test
Version:        2.6
Release:        1%{?dist}.20110530svn%{svn_rev}
Summary:        Test images for dcm4che2

License:        MPLv1.1 or GPLv2 or LGPLv2
URL:            http://www.dcm4che.org/confluence/display/proj/The+Project
BuildArch:      noarch

# Generated from an svn checkout: TODO: use svn export next time
# svn export https://dcm4che.svn.sourceforge.net/svnroot/dcm4che/dcm4che2-test/tags/dcm4che2-test-2.6
# tar -cvzf dcm4che2-test-2.6.tar.gz dcm4che2-test-2.6/
Source0:        dcm4che2-test-%{version}.tar.gz

BuildRequires:    jpackage-utils
BuildRequires:    java-devel
BuildRequires:    maven
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-release-plugin
BuildRequires:    maven-resources-plugin
BuildRequires:    maven-surefire-plugin

Requires:       jpackage-utils
Requires:       java

Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils

%description
DCM4CHE Test Data and Libraries

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n dcm4che2-test-2.6

%build
mvn-rpmbuild -X install javadoc:aggregate 

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p  %{name}-image/target/%{name}-image-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-image.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/ $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

install -pm 644 %{name}-image/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-image.pom

# note that the artifact id is %%{name}-image, not dcm4che2-test-image
%add_to_maven_depmap org.dcm4che.test %{name}-image %{version} JPP %{name}-image

# Check on this: there is no jar for the -test pom, do we need a add_to_maven_depmap here?
%add_to_maven_depmap org.dcm4che.test dcm4che2-test %{version} JPP %{name}

find $RPM_BUILD_ROOT%{_javadocdir}/%{name} -name "javadoc.sh" -exec chmod a-x '{}' \;

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%{_mavenpomdir}/*.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}-image.jar

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Mon May 30 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.6-0.1.20110530svn15516
- Edited find command
- Corrected versioning
- Corrected License versions
- Corrected depmap, and java bits : thanks Stanislav Ochotnicky!
- made changes using macros
- Correct add to maven depmap command
- initial rpm build
