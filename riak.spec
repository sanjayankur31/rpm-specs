%global realname riak
%global upstream basho
%global debug_package %{nil}
%global git_tag 95c5cb6
%global patchnumber 0


Name:		%{realname}
Version:	1.1.4
Release:	2%{?dist}
Summary:	Dynamo-inspired key/value store
Group:		Applications/Databases
License:	ASL 2.0
URL:		http://wiki.basho.com/Riak.html
# wget --content-disposition https://github.com/basho/riak/tarball/riak-1.1.4
Source0:	%{upstream}-%{realname}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
Source1:	%{name}.tmpfiles.conf
Source2:	%{name}.init
Source3:	%{name}.service
Patch1:		riak-0001-Add-OTP-version-R15-to-allowed-version-regex.patch
Patch2:		riak-0002-Don-t-try-to-install-dependencies-Fedora-EPEL-specif.patch
Patch3:		riak-0003-Rename-basho-patches-directory.patch
BuildRequires:	erlang-rebar
BuildRequires:	erlang-cluster_info
BuildRequires:	erlang-eper
BuildRequires:	erlang-riak_control
BuildRequires:	erlang-riak_kv
BuildRequires:	erlang-riak_search

Requires:	erlang-cluster_info
Requires:	erlang-eper
Requires:	erlang-riak_control
Requires:	erlang-riak_kv
Requires:	erlang-riak_search
# FIXME - I'll add luwak backend later
#Requires:	erlang-luwak

#Initscripts
%if 0%{?fedora}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(post): chkconfig
Requires(preun): chkconfig initscripts
%endif

# Users and groups
Requires(pre): shadow-utils


%description
Riak is a Dynamo-inspired key/value store that scales predictably and easily.
Riak also simplifies development by giving developers the ability to quickly
prototype, test, and deploy their applications.

A truly fault-tolerant system, Riak has no single point of failure. No machines
are special or central in Riak, so developers and operations professionals can
decide exactly how fault-tolerant they want and need their applications to be.


%prep
echo "WM " %{webmachinever}
%setup -q -n %{upstream}-%{realname}-83ec281
%patch1 -p1 -b .r15b
%patch2 -p1 -b .nodeps
%patch3 -p1 -b .basho-patches-rename

gzip -d doc/man/man1/*.1.gz
sed -i -e "s,\\\n,,g" doc/man/man1/riak-admin.1

# Override the default vars.config with platform specific settings
cat > rel/vars.config <<EOF
% Platform-specific installation paths
{platform_bin_dir,	"%{_bindir}"}.
{platform_data_dir,	"%{_localstatedir}/lib/%{name}"}.
{platform_etc_dir,	"%{_sysconfdir}/%{name}"}.
{platform_lib_dir,	"%{_libdir}/%{name}"}.
{platform_log_dir,	"%{_localstatedir}/log/%{name}"}.

%%
%% etc/app.config
%%
{web_ip,		"127.0.0.1"}.
{web_port,		8098}.
{handoff_port,		8099}.
{pb_ip,			"127.0.0.1"}.
{pb_port,		8087}.
{ring_state_dir,	"%{_localstatedir}/lib/%{name}/ring"}.
{bitcask_data_root,	"%{_localstatedir}/lib/%{name}/bitcask"}.
{leveldb_data_root,	"%{_localstatedir}/lib/%{name}/leveldb"}.
{sasl_error_log,	"%{_localstatedir}/log/%{name}/sasl-error.log"}.
{sasl_log_dir,		"%{_localstatedir}/log/%{name}/sasl"}.
{mapred_queue_dir,	"%{_localstatedir}/lib/%{name}/mr_queue"}.

%% riak_search
{merge_index_data_root,	"%{_localstatedir}/lib/%{name}/merge_index"}.

%% Javascript VMs
{map_js_vms,	8}.
{reduce_js_vms,	6}.
{hook_js_vms,	2}.

%%
%% etc/vm.args
%%
{node,		"riak@127.0.0.1"}.
{crash_dump,	"%{_localstatedir}/log/%{name}/erl_crash.dump"}.

%%
%% bin/riak
%%
{runner_script_dir,	"%{_bindir}"}.
{runner_base_dir,	"%{_libdir}/%{name}"}.
{runner_etc_dir,	"%{_sysconfdir}/%{name}"}.
{runner_log_dir,	"%{_localstatedir}/log/%{name}"}.
{pipe_dir,		"%{_localstatedir}/run/%{name}/"}.
{runner_user,		"%{name}"}.
EOF


%build
rebar compile generate -v


%install
# Install Erlang VM config files
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -D -p -m 0644 rel/riak/etc/app.config %{buildroot}%{_sysconfdir}/%{name}/app.config
install -D -p -m 0644 rel/riak/etc/vm.args %{buildroot}%{_sysconfdir}/%{name}/vm.args

# Install init-script or systemd-service
%if 0%{?fedora}
install -D -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
%else
install -D -p -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
%endif

# Install runtime scripts
install -p -m 0755 -D  rel/riak/bin/%{name} %{buildroot}%{_bindir}/%{name}
install -p -m 0755 -D  rel/riak/bin/%{name}-admin %{buildroot}%{_bindir}/%{name}-admin
install -p -m 0755 -D  rel/riak/bin/search-cmd %{buildroot}%{_bindir}/search-cmd

# Install man-pages
install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644 doc/man/man1/%{name}.1 %{buildroot}%{_mandir}/man1/
install -p -m 0644 doc/man/man1/%{name}-admin.1 %{buildroot}%{_mandir}/man1/
install -p -m 0644 doc/man/man1/search-cmd.1 %{buildroot}%{_mandir}/man1/

# Install remaining Erlang files
mkdir -p %{buildroot}%{_libdir}/erlang/lib/%{name}-%{version}/ebin
install -p -m 0644 ebin/%{name}.app %{buildroot}%{_libdir}/erlang/lib/%{name}-%{version}/ebin/
install -p -m 0644 ebin/etop_txt.beam %{buildroot}%{_libdir}/erlang/lib/%{name}-%{version}/ebin/

# Make room for temporary files, logs, and data
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/bitcask/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/dets/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/leveldb/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/merge_index/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/mr_queue/
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}/ring/
mkdir -p %{buildroot}/%{_localstatedir}/log/%{name}/
mkdir -p %{buildroot}/%{_localstatedir}/log/%{name}/sasl/
mkdir -p %{buildroot}/%{_localstatedir}/run/%{name}/

# Install Erlang release binary data
mkdir -p %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/riak/releases/RELEASES %{buildroot}/%{_libdir}/%{name}/releases/
install -m 644 rel/riak/releases/start_erl.data %{buildroot}/%{_libdir}/%{name}/releases/
install -m 644 rel/riak/releases/1.1.4/riak.boot %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/riak/releases/1.1.4/riak.rel %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/riak/releases/1.1.4/riak.script %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/riak/releases/1.1.4/start_clean.boot %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/riak/releases/1.1.4/start_clean.rel %{buildroot}/%{_libdir}/%{name}/releases/%{version}/
install -m 644 rel/riak/releases/1.1.4/start_clean.script %{buildroot}/%{_libdir}/%{name}/releases/%{version}/

# Install nodetool
install -D -p -m 755 rel/riak/erts-5.9.1/bin/nodetool %{buildroot}/%{_libdir}/erlang/erts-5.9.1/bin/nodetool

# Make compat symlinks
cd %{buildroot}/%{_libdir}/%{name}
ln -s %{_libdir}/erlang/lib lib
ln -s %{_libdir}/erlang/erts-5.9.1 erts-5.9.1


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
useradd -r -g %{name} -d %{_localstatedir}/run/%{name} -s /sbin/nologin \
-c "Riak - a dynamo-inspired key/value store" %{name} 2>/dev/null || :


%post
%if 0%{?fedora}
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
/sbin/chkconfig --add %{name}
%endif


%preun
%if 0%{?fedora}
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable %{name}.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
fi
%else
if [ $1 = 0 ]; then
 /sbin/service %{name} stop > /dev/null 2>&1
 /sbin/chkconfig --del %{name}
fi
%endif


%files
%doc doc/[abdr]* releasenotes/ LICENSE NOTICE README.org RELEASE-NOTES.org THANKS
%if 0%{?fedora}
%{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/app.config
%config(noreplace) %{_sysconfdir}/%{name}/vm.args
%{_bindir}/%{name}
%{_bindir}/%{name}-admin
%{_bindir}/search-cmd
%dir %{_libdir}/erlang/lib/%{name}-%{version}
%dir %{_libdir}/erlang/lib/%{name}-%{version}/ebin
%{_libdir}/erlang/lib/%{name}-%{version}/ebin/%{name}.app
%{_libdir}/erlang/lib/%{name}-%{version}/ebin/etop_txt.beam
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/%{name}-admin.1.gz
%{_mandir}/man1/search-cmd.1.gz
%{_libdir}/%{name}/
%{_libdir}/erlang/erts-5.9.1/bin/nodetool
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/bitcask/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/dets/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/leveldb/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/merge_index/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/mr_queue/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/lib/%{name}/ring/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/log/%{name}/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/log/%{name}/sasl/
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/run/%{name}/


%changelog
* Tue Aug 14 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.4-2
- Fixed lots of packaging issues (thanks to Ankur Sinha for noticing them)

* Fri Jul 20 2012 Peter Lemenkov <lemenkov@gmail.com> - 1.1.4-1
- Ver. 1.1.4

* Wed Oct 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.13.0-1
- Initial build

