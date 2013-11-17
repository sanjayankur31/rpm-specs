Name:           fiji
Version:        20110608
Release:        1%{?dist}.git
Summary:        Fiji Is Just ImageJ

License:        GPLv2 
URL:            http://pacific.mpi-cbg.de/wiki/index.php/Fiji
# git clone contrib@pacific.mpi-cbg.de:/srv/git/fiji.git
# tar -cvzf fiji-20110608-git.tar.gz fiji/
Source0:        %{name}-%{version}-git.tar.gz

# why does it look for tools.jar!?
BuildRequires:  java-devel java-1.6.0-openjdk-devel jpackage-utils
BuildRequires:  vecmath
Requires:       java

%description
Fiji will provide an easy way to set up Java+ImageJA+TrakEM2+VIB+a lot of
other plugins that are useful to biologists, geologists and every other
scientist who wants to process images.


%prep
%setup -q -n %{name}

%build
# to set the JAVA_HOME variable
source %{_datadir}/java-utils/java-functions
set_jvm
echo $JAVA_HOME
export JAVA_HOME

sh Build.sh fiji

%install
rm -rf $RPM_BUILD_ROOT


%files
%doc



%changelog
* Wed Jun 08 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110608-1.git
- initial rpm build
