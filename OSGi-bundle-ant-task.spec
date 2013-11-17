%global svn_rev 1242
Name:           OSGi-bundle-ant-task
Version:        0.2.0
Release:        0.3.svn%{svn_rev}%{?dist}
Summary:        A wrapper around Bnd to allow easy bundle creation from ant builds

License:        BSD
URL:            https://opensource.luminis.net/wiki/display/SITE/OSGi+Bundle+Ant+Task
# svn export -r 1242 https://opensource.luminis.net/svn/BUNDLES/releases/build-plugin-0.2.0/  OSGi-bundle-ant-task
# tar -cvzf OSGi-bundle-ant-task.tar.gz OSGi-bundle-ant-task/
Source0:        %{name}.tar.gz
Source1:        %{name}-bsd.txt
Patch0:         %{name}-build-xml.patch

BuildArch:      noarch
BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  aqute-bndlib ant

# for jar
BuildRequires:  java-1.6.0-openjdk-devel

Requires:       jpackage-utils
Requires:       java

%description
A wrapper around Bnd to allow easy bundle creation from ant builds

%prep
%setup -q -n %{name}
%patch0 -p0

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;
cp %{SOURCE1} .

%build
export CLASSPATH=$(build-classpath aqute-bndlib ant)
ant dist
%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -pa dist/lib/net.luminis.build.plugin-0.2.0.jar  $RPM_BUILD_ROOT%{_javadir}/net.luminis.build.plugin.jar

%files
%doc %{name}-bsd.txt
%{_javadir}/*

%changelog
* Sun Jul 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.0-0.3.svn1242
- correct versioning
- correct svn command
- add license

* Fri Jul 08 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.0-0.2svn1242
- update patch to fix build.xml

* Wed Jul 06 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.0-0.1svn1242
- initial rpm build
