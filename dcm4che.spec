Name:       dcm4che
Version:    2.0.25
Release:    1%{?dist}
Summary:    A DICOM implementation in Java

#Group:       
License:    MPLv1.1
URL:        http://www.dcm4che.org/confluence/display/proj/The+Project
# Follow the link at http://sourceforge.net/projects/dcm4che/files/dcm4che2/2.0.25/
Source0:    http://downloads.sourceforge.net/dcm4che/dcm4che2/%{version}/%{name}-%{version}-src.zip
# additional depmaps for ones that dont have poms etc
# example: jai_imageio
Source1:    dcm4che.depmap

# Add a property section to pom to use UTF-8 encoding
# Add versioning for some plugins to remove warnings
# Please do check the patch for correct versioning of
# plugins for future builds
Patch1:     dcm4che-encoding-pom.patch

BuildArch:      noarch

BuildRequires:    jpackage-utils
BuildRequires:    java-devel
BuildRequires:    maven
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-release-plugin
BuildRequires:    maven-resources-plugin
BuildRequires:    maven-repository-plugin
BuildRequires:    maven-surefire-plugin
BuildRequires:    maven-surefire-provider-junit4
BuildRequires:    jai-imageio-core
#BuildRequires:    junit
#BuildRequires:    junit4
BuildRequires:    dcm4che-test

Requires:       jpackage-utils
Requires:       java

Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils


%description
dcm4che is a collection of open source applications and utilities
for health care IT. These applications have been developed in
the Java programming language for performance and portability;
supporting deployment on JDK 1.4 and up.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1

JAR_files=""
for j in $(find -name \*.jar); do
    if [ ! -L $j ] ; then
        JAR_files="$JAR_files $j"
    fi
done
if [ ! -z "$JAR_files" ] ; then
    echo "These JAR files should be deleted and symlinked to system JAR files: $JAR_files"
    exit 1
fi
#find -name '*.class' -exec rm -fv '{}' \;
#find -name '*.jar' -exec rm -fv '{}' \;

%build
mvn-rpmbuild -X -Dmaven.local.depmap.file="%{SOURCE1}" \
    install javadoc:aggregate


%install
# more than 2 jars, create subdir
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}

# Should these be in different sub packages?
# Install jar files
# install poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap %{name} %{name} %{version} JPP/%{name} %{name}

install -pm 644 %{name}-tool/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool.pom
%add_to_maven_depmap %{name}.tool %{name}-tool %{version} JPP/%{name} %{name}-tool

cp -pv %{name}-core-test-dictionary/target/%{name}-core-test-dictionary-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-core-test-dictionary.jar
install -pm 644 %{name}-core-test-dictionary/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-core-test-dictionary.pom
%add_to_maven_depmap %{name} %{name}-core-test-dictionary %{version} JPP/%{name} %{name}-core-test-dictionary

cp -pv %{name}-imageio/target/%{name}-imageio-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-imageio.jar
install -pm 644 %{name}-imageio/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-imageio.pom
%add_to_maven_depmap %{name} %{name}-imageio %{version} JPP/%{name} %{name}-imageio

cp -pv %{name}-image/target/%{name}-image-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-image.jar
install -pm 644 %{name}-image/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-image.pom
%add_to_maven_depmap %{name} %{name}-image %{version} JPP/%{name} %{name}-image

cp -pv %{name}-imageio-rle/target/%{name}-imageio-rle-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-imageio-rle.jar
install -pm 644 %{name}-imageio-rle/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-imageio-rle.pom
%add_to_maven_depmap %{name} %{name}-imageio-rle %{version} JPP/%{name} %{name}-imageio-rle

cp -pv %{name}-hp/target/%{name}-hp-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-hp.jar
# Query: the pom.xml does not have a group id!
install -pm 644 %{name}-hp/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-hp.pom
%add_to_maven_depmap %{name} %{name}-hp %{version} JPP/%{name} %{name}-hp

cp -pv %{name}-iod/target/%{name}-iod-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-iod.jar
# Query: the pom.xml does not have a group id!
install -pm 644 %{name}-iod/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-iod.pom
%add_to_maven_depmap %{name} %{name}-iod %{version} JPP/%{name} %{name}-iod

cp -pv %{name}-code/target/%{name}-code-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-code.jar
# Query: the pom.xml does not have a group id!
install -pm 644 %{name}-code/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-code.pom
%add_to_maven_depmap %{name} %{name}-iod %{version} JPP/%{name} %{name}-code

cp -pv %{name}-soundex/target/%{name}-soundex-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-soundex.jar
install -pm 644 %{name}-soundex/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-soundex.pom
%add_to_maven_depmap %{name} %{name}-soundex %{version} JPP/%{name} %{name}-soundex

cp -pv %{name}-core/target/%{name}-core-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-core.jar
install -pm 644 %{name}-core/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-core.pom
%add_to_maven_depmap %{name} %{name}-core %{version} JPP/%{name} %{name}-core

cp -pv %{name}-base64/target/%{name}-base64-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-base64.jar
install -pm 644 %{name}-base64/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-base64.pom
%add_to_maven_depmap %{name} %{name}-base64 %{version} JPP/%{name} %{name}-base64

cp -pv %{name}-net/target/%{name}-net-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-net.jar
install -pm 644 %{name}-net/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-net.pom
%add_to_maven_depmap %{name} %{name} %{version}-net JPP/%{name} %{name}-net

cp -pv %{name}-filecache/target/%{name}-filecache-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-filecache.jar
install -pm 644 %{name}-filecache/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-filecache.pom
%add_to_maven_depmap %{name} %{name}-filecache %{version} JPP/%{name} %{name}-filecache

cp -pv %{name}-audit/target/%{name}-audit-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-audit.jar
# Query: the pom.xml does not have a group id!
install -pm 644 %{name}-audit/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-audit.pom
%add_to_maven_depmap %{name} %{name}-audit %{version} JPP/%{name} %{name}-audit

cp -pv %{name}-tool/%{name}-tool-rgb2ybr/target/%{name}-tool-rgb2ybr-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-rgb2ybr.jar
install -pm 644 %{name}-tool/%{name}-tool-rgb2ybr/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-rgb2ybr.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-rgb2ybr %{version} JPP/%{name} %{name}-tool-rgb2ybr

cp -pv %{name}-tool/%{name}-tool-fixjpegls/target/%{name}-tool-fixjpegls-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-fixjpegls.jar
install -pm 644 %{name}-tool/%{name}-tool-fixjpegls/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-fixjpegls.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-fixjpegls %{version} JPP/%{name} %{name}-tool-fixjpegls

cp -pv %{name}-tool/%{name}-tool-dcm2txt/target/%{name}-tool-dcm2txt-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcm2txt.jar
install -pm 644 %{name}-tool/%{name}-tool-dcm2txt/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcm2txt.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcm2txt %{version} JPP/%{name} %{name}-tool-dcm2txt

cp -pv %{name}-tool/%{name}-tool-dcm2jpg/target/%{name}-tool-dcm2jpg-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcm2jpg.jar
install -pm 644 %{name}-tool/%{name}-tool-dcm2jpg/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcm2jpg.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcm2jpg %{version} JPP/%{name} %{name}-tool-dcm2jpg

cp -pv %{name}-tool/%{name}-tool-dcmecho/target/%{name}-tool-dcmecho-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmecho.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmecho/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmecho.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmecho %{version} JPP/%{name} %{name}-tool-dcmecho

cp -pv %{name}-tool/%{name}-tool-xml2dcm/target/%{name}-tool-xml2dcm-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-xml2dcm.jar
install -pm 644 %{name}-tool/%{name}-tool-xml2dcm/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-xml2dcm.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-xml2dcm %{version} JPP/%{name} %{name}-tool-xml2dcm

cp -pv %{name}-tool/%{name}-tool-jpg2dcm/target/%{name}-tool-jpg2dcm-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-jpg2dcm.jar
install -pm 644 %{name}-tool/%{name}-tool-jpg2dcm/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-jpg2dcm.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-jpg2dcm %{version} JPP/%{name} %{name}-tool-jpg2dcm

cp -pv %{name}-tool/%{name}-tool-dcmmwl/target/%{name}-tool-dcmmwl-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmmwl.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmmwl/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmmwl.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmmwl %{version} JPP/%{name} %{name}-tool-dcmmwl

cp -pv %{name}-tool/%{name}-tool-chess3d/target/%{name}-tool-chess3d-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-chess3d.jar
install -pm 644 %{name}-tool/%{name}-tool-chess3d/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-chess3d.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-chess3d %{version} JPP/%{name} %{name}-tool-chess3d

cp -pv %{name}-tool/%{name}-tool-dcmof/target/%{name}-tool-dcmof-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmof.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmof/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmof.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmof %{version} JPP/%{name} %{name}-tool-dcmof

cp -pv %{name}-tool/%{name}-tool-dcmgpwl/target/%{name}-tool-dcmgpwl-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmgpwl.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmgpwl/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmgpwl.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmgpwl %{version} JPP/%{name} %{name}-tool-dcmgpwl

cp -pv %{name}-tool/%{name}-tool-dcmwado/target/%{name}-tool-dcmwado-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmwado.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmwado/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmwado.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmwado %{version} JPP/%{name} %{name}-tool-dcmwado

cp -pv %{name}-tool/%{name}-tool-pdf2dcm/target/%{name}-tool-pdf2dcm-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-pdf2dcm.jar
install -pm 644 %{name}-tool/%{name}-tool-pdf2dcm/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-pdf2dcm.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-pdf2dcm %{version} JPP/%{name} %{name}-tool-pdf2dcm

cp -pv %{name}-tool/%{name}-tool-dcmrcv/target/%{name}-tool-dcmrcv-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmrcv.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmrcv/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmrcv.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmrcv %{version} JPP/%{name} %{name}-tool-dcmrcv

cp -pv %{name}-tool/%{name}-tool-dcmhpqr/target/%{name}-tool-dcmhpqr-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmhpqr.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmhpqr/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmhpqr.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmhpqr %{version} JPP/%{name} %{name}-tool-dcmhpqr

cp -pv %{name}-tool/%{name}-tool-dcm2dcm/target/%{name}-tool-dcm2dcm-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcm2dcm.jar
install -pm 644 %{name}-tool/%{name}-tool-dcm2dcm/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcm2dcm.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcm2dcm %{version} JPP/%{name} %{name}-tool-dcm2dcm

cp -pv %{name}-tool/%{name}-tool-dcmups/target/%{name}-tool-dcmups-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmups.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmups/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-%{name}-tool-dcmups.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmups %{version} JPP/%{name} %{name}-tool-dcmups

cp -pv %{name}-tool/%{name}-tool-txt2dcmsr/target/%{name}-tool-txt2dcmsr-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-txt2dcmsr.jar
install -pm 644 %{name}-tool/%{name}-tool-txt2dcmsr/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-txt2dcmsr.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-txt2dcmsr %{version} JPP/%{name} %{name}-tool-txt2dcmsr

cp -pv %{name}-tool/%{name}-tool-dcm2xml/target/%{name}-tool-dcm2xml-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcm2xml.jar
install -pm 644 %{name}-tool/%{name}-tool-dcm2xml/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcm2xml.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcm2xml %{version} JPP/%{name} %{name}-tool-dcm2xml

cp -pv %{name}-tool/%{name}-tool-dcmsnd/target/%{name}-tool-dcmsnd-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmsnd.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmsnd/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmsnd.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmsnd %{version} JPP/%{name} %{name}-tool-dcmsnd

cp -pv %{name}-tool/%{name}-tool-dcmdir/target/%{name}-tool-dcmdir-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmdir.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmdir/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmdir.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmdir %{version} JPP/%{name} %{name}-tool-dcmdir

cp -pv %{name}-tool/%{name}-tool-logger/target/%{name}-tool-logger-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-logger.jar
install -pm 644 %{name}-tool/%{name}-tool-logger/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-logger.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-logger %{version} JPP/%{name} %{name}-tool-logger

cp -pv %{name}-tool/%{name}-tool-dcmmv/target/%{name}-tool-dcmmv-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmmv.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmmv/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmmv.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmmv %{version} JPP/%{name} %{name}-tool-dcmmv

cp -pv %{name}-tool/%{name}-tool-dcmqr/target/%{name}-tool-dcmqr-2.0.25.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tool-dcmqr.jar
install -pm 644 %{name}-tool/%{name}-tool-dcmqr/pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-tool-dcmqr.pom
%add_to_maven_depmap %{name}.tool %{name}-tool-dcmqr %{version} JPP/%{name} %{name}-tool-dcmqr

# Install java docs
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/ $RPM_BUILD_ROOT%{_javadocdir}/%{name}

find $RPM_BUILD_ROOT%{_javadocdir}/%{name} -name "javadoc.sh" -exec chmod a-x '{}' \;

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%{_mavenpomdir}/JPP-%{name}*
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}/

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Tue May 10 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.0.25-1
- Initial rpm build

