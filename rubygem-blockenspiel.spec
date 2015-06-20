# Generated from blockenspiel-0.4.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name blockenspiel

Name: rubygem-%{gem_name}
Version: 0.4.5
Release: 1%{?dist}
Summary: Blockenspiel is a helper library designed to make it easy to implement DSL blocks
Group: Development/Languages
License: MIT
URL: http://dazuma.github.com/blockenspiel
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) > 1.3.1
BuildRequires: ruby(release)
BuildRequires: rubygems-devel > 1.3.1
BuildRequires: ruby-devel >= 1.8.7
Provides: rubygem(%{gem_name}) = %{version}

%description
Blockenspiel is a helper library designed to make it easy to implement DSL
blocks. It is designed to be comprehensive and robust, supporting most common
usage patterns, and working correctly in the presence of nested blocks and
multithreading.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/lib
#cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}/%{gem_instdir}/ext/

%check
pushd .%{gem_instdir}

popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_instdir}/ext
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Blockenspiel.rdoc
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/ImplementingDSLblocks.rdoc
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/Version
%exclude %{gem_instdir}/test/

%changelog
* Thu Apr 10 2014 Achilleas Pipinellis <axilleas@fedoraproject.org> - 0.4.5-1
- Initial package
