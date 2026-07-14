Summary: I2P router written in C++
Name: i2pd
Version: 2.60.0
Release: 1
License: BSD
Group: System/Servers
Url: https://github.com/PurpleI2P/i2pd
Source0: https://github.com/PurpleI2P/i2pd/archive/%{version}/%{name}-%{version}.tar.gz
Source100: i2pd.rpmlintrc
BuildRequires: chrpath
BuildRequires: cmake >= 3.22
BuildRequires: make
BuildRequires: boost-devel
BuildRequires: glibc-devel
BuildRequires: miniupnpc-devel
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(zlib)

BuildSystem:	cmake
BuildOption:	-DWITH_LIBRARY=OFF
BuildOption:	-DWITH_UPNP=ON
BuildOption:	-DWITH_HARDENING=ON
BuildOption:	-DBUILD_SHARED_LIBS:BOOL=OFF
#BuildOption:	-DWITH_AESNI=OFF
#BuildOption:	-DWITH_AVX=OFF

%description
C++ implementation of I2P.

%files
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%dir %{_sysconfdir}/%{name}/tunnels.conf.d
%config(noreplace) %{_sysconfdir}/i2pd/tunnels.conf.d/*
%{_datadir}/%{name}/certificates
%{_unitdir}/%{name}.service
%{_sysusersdir}/*.conf
%dir %attr(0700,i2pd,i2pd) %{_localstatedir}/log/%{name}
%dir %attr(0700,i2pd,i2pd) %{_sharedstatedir}/%{name}
%{_sharedstatedir}/%{name}/certificates

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}/build


%install -a
#chrpath -d %%{buildroot}%%{_bindir}/%%{name}
install -D -m 755 ../contrib/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -D -m 755 ../contrib/tunnels.conf %{buildroot}%{_sysconfdir}/%{name}/tunnels.conf
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/%{name}/tunnels.conf.d
%{__cp} -r ../contrib/certificates/ %{buildroot}%{_datadir}/%{name}/certificates
%{__cp} -r ../contrib/tunnels.d/ %{buildroot}%{_sysconfdir}/%{name}/tunnels.conf.d
install -D -m 644 ../contrib/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -d -m 700 %{buildroot}%{_sharedstatedir}/%{name}
install -d -m 700 %{buildroot}%{_localstatedir}/log/%{name}
ln -s %{_datadir}/%{name}/certificates %{buildroot}%{_sharedstatedir}/%{name}/certificates
ln -s %{_datadir}/%{name}/tunnels.conf.d %{buildroot}%{_sysconfdir}/%{name}/tunnels.conf.d

mkdir -p %{buildroot}%{_sysusersdir}
cat >%{buildroot}%{_sysusersdir}/%{name}.conf <<EOF
g i2pd
u i2pd - "I2P Service" %{_sharedstatedir}/%{name} %{_bindir}/nologin
EOF

# Fix perms
chmod -x %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
chmod -x %{buildroot}%{_sysconfdir}/%{name}/tunnels.conf
