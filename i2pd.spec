Name:           i2pd
Version:        2.30.0
Release:        1
Summary:        I2P router written in C++
Group:          System/Servers

License:        BSD
URL:            https://github.com/PurpleI2P/i2pd
Source0:        https://github.com/PurpleI2P/i2pd/archive/%{version}/%name-%version.tar.gz

BuildRequires:  cmake
BuildRequires:  glibc-devel
BuildRequires:  chrpath
BuildRequires:  gcc-c++
BuildRequires:  zlib-devel
BuildRequires:  boost-devel
BuildRequires:  openssl-devel
BuildRequires:  miniupnpc-devel
BuildRequires:  systemd-units
BuildRequires:  rpm-helper

Requires:	systemd
Requires(pre):  %{_sbindir}/useradd %{_sbindir}/groupadd

%description
C++ implementation of I2P.

%prep
%autosetup -p1


%build
pushd build
%cmake \
    -DWITH_LIBRARY=OFF \
    -DWITH_UPNP=ON \
    -DWITH_AESNI=OFF \
    -DWITH_AVX=OFF \
    -DWITH_HARDENING=ON \
    -DBUILD_SHARED_LIBS:BOOL=OFF

%make_build
popd

%install
pushd build/build
chrpath -d i2pd
install -D -m 755 i2pd %{buildroot}%{_sbindir}/i2pd
install -D -m 755 %{_builddir}/%{name}-%{version}/contrib/i2pd.conf %{buildroot}%{_sysconfdir}/i2pd/i2pd.conf
install -D -m 755 %{_builddir}/%{name}-%{version}/contrib/tunnels.conf %{buildroot}%{_sysconfdir}/i2pd/tunnels.conf
install -d -m 755 %{buildroot}%{_datadir}/i2pd
install -d -m 755 %{buildroot}%{_datadir}/i2pd/tunnels.conf.d
%{__cp} -r %{_builddir}/%{name}-%{version}/contrib/certificates/ %{buildroot}%{_datadir}/i2pd/certificates
%{__cp} -r %{_builddir}/%{name}-%{version}/contrib/tunnels.d/ %{buildroot}%{_sysconfdir}/i2pd/tunnels.conf.d
install -D -m 644 %{_builddir}/%{name}-%{version}/contrib/rpm/i2pd.service %{buildroot}%{_unitdir}/i2pd.service
install -d -m 700 %{buildroot}%{_sharedstatedir}/i2pd
install -d -m 700 %{buildroot}%{_localstatedir}/log/i2pd
ln -s %{_datadir}/%{name}/certificates %{buildroot}%{_sharedstatedir}/i2pd/certificates
ln -s %{_datadir}/i2pd/tunnels.conf.d %{buildroot}%{_sysconfdir}/i2pd/tunnels.conf.d
popd

%pre
getent group i2pd >/dev/null || %{_sbindir}/groupadd -r i2pd
getent passwd i2pd >/dev/null || \
  %{_sbindir}/useradd -r -g i2pd -s %{_sbindir}/nologin \
                      -d %{_sharedstatedir}/i2pd -c 'I2P Service' i2pd


%post
%systemd_post i2pd.service


%preun
%systemd_preun i2pd.service


%postun
%systemd_postun_with_restart i2pd.service


%files
%doc LICENSE README.md
%{_sbindir}/i2pd
%{_datadir}/i2pd/certificates
%config(noreplace) %{_sysconfdir}/i2pd/*
%config(noreplace) %{_sysconfdir}/i2pd/tunnels.conf.d/*
%{_unitdir}/i2pd.service
%dir %attr(0700,i2pd,i2pd) %{_localstatedir}/log/i2pd
%dir %attr(0700,i2pd,i2pd) %{_sharedstatedir}/i2pd
%{_sharedstatedir}/i2pd/certificates


%changelog
* Tue Feb 25 2020 r4sas <r4sas@i2pmail.org> - 2.30.0
- update to 2.30.0

* Tue Aug 27 2019 r4sas <r4sas@i2pmail.org> - 2.28.0
- update to 2.28.0
