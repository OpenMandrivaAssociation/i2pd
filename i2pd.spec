%define i2pduser _i2pd
%define debug_package %nil
%define _i2pd_root /run/%name

Name:		i2pd
Summary:	Full C++ implementation of I2P router
Version:	2.11.0
Release:	1
License:	BSD-3-Clause
Group:		System/Servers
Url:		https://github.com/PurpleI2P/i2pd

Source0:	https://github.com/PurpleI2P/i2pd/archive/%{version}.tar.gz
Source2:	%name.logrotate
Source3:	i2p.conf
Source4:	tunnels.conf

Requires(pre):	rpm-helper

BuildRequires:	miniupnpc-devel
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	zlib-devel
BuildRequires:	openssl-devel

%description
I2P router written in C++

%prep
%setup
%apply_patches

%build
pushd build
cmake \
      -DWITH_BINARY=ON \
      -DWITH_LIBRARY=ON \
      -DWITH_STATIC=OFF \
      -DWITH_UPNP=ON \
      -DWITH_AESNI=OFF \
      -DWITH_HARDENING=ON \
      -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DWITH_PCH=OFF .

%make
popd

%install
pushd build
%makeinstall_std
popd

install -pDm 644 contrib/rpm/i2pd.service %buildroot%_unitdir/%name.service
rm -rf %{buildroot}/usr/src
rm -f %{buildroot}/usr/lib/libi2pd.a %{buildroot}/usr/LICENSE
sed -i "s!PIDFile=/var/lib/i2pd/i2pd.pid!PIDFile=/run/i2pd/i2pd.pid!g" %{buildroot}%{_unitdir}/%{name}.service

%pre
%_pre_useradd %{name} /run/%{name} /sbin/nologin
%_pre_groupadd %{name} %{name}

%post
%_post_service %{name}

%postun
%_postun_userdel %{name}
%_postun_groupdel %{name} %{name}

%files
%doc LICENSE README.md docs/configuration.md
%_bindir/%name
%_unitdir/%name.service
