Name:           i2pd
Version:        2.55.0
Release:        1
Summary:        I2P router written in C++
Group:          System/Servers

License:        BSD
URL:            https://github.com/PurpleI2P/i2pd
Source0:        https://github.com/PurpleI2P/i2pd/archive/%{version}/%name-%version.tar.gz

BuildRequires:  glibc-devel
BuildRequires:  chrpath
BuildRequires:  zlib-devel
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(openssl)
BuildRequires:  miniupnpc-devel

BuildSystem:	cmake
BuildOption:	-DWITH_LIBRARY=OFF
BuildOption:	-DWITH_UPNP=ON
BuildOption:	-DWITH_AESNI=OFF
BuildOption:	-DWITH_AVX=OFF
BuildOption:	-DWITH_HARDENING=ON
BuildOption:	-DBUILD_SHARED_LIBS:BOOL=OFF

%description
C++ implementation of I2P.

%prep
%autosetup -p1 -n %{name}-%{version}/build

%install -a
chrpath -d %{buildroot}%{_bindir}/i2pd
install -D -m 755 ../contrib/i2pd.conf %{buildroot}%{_sysconfdir}/i2pd/i2pd.conf
install -D -m 755 ../contrib/tunnels.conf %{buildroot}%{_sysconfdir}/i2pd/tunnels.conf
install -d -m 755 %{buildroot}%{_datadir}/i2pd
install -d -m 755 %{buildroot}%{_datadir}/i2pd/tunnels.conf.d
%{__cp} -r ../contrib/certificates/ %{buildroot}%{_datadir}/i2pd/certificates
%{__cp} -r ../contrib/tunnels.d/ %{buildroot}%{_sysconfdir}/i2pd/tunnels.conf.d
install -D -m 644 ../contrib/i2pd.service %{buildroot}%{_unitdir}/i2pd.service
install -d -m 700 %{buildroot}%{_sharedstatedir}/i2pd
install -d -m 700 %{buildroot}%{_localstatedir}/log/i2pd
ln -s %{_datadir}/%{name}/certificates %{buildroot}%{_sharedstatedir}/i2pd/certificates
ln -s %{_datadir}/i2pd/tunnels.conf.d %{buildroot}%{_sysconfdir}/i2pd/tunnels.conf.d

mkdir -p %{buildroot}%{_sysusersdir}
cat >%{buildroot}%{_sysusersdir}/%{name}.conf <<EOF
g i2pd
u i2pd - "I2P Service" %{_sharedstatedir}/i2pd %{_bindir}/nologin
EOF

%files
%{_bindir}/i2pd
%{_datadir}/i2pd/certificates
%config(noreplace) %{_sysconfdir}/i2pd/*
%config(noreplace) %{_sysconfdir}/i2pd/tunnels.conf.d/*
%{_unitdir}/i2pd.service
%dir %attr(0700,i2pd,i2pd) %{_localstatedir}/log/i2pd
%dir %attr(0700,i2pd,i2pd) %{_sharedstatedir}/i2pd
%{_sharedstatedir}/i2pd/certificates
%{_sysusersdir}/*.conf
