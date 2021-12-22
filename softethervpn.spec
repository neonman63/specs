%define majorversion 4
%define minorversion 38
%define buildversion 9760
%define dateversion 2021.08.17
%define buildrelease rtm

Name:           softethervpn
Version:        %{majorversion}.%{minorversion}.%{buildversion}
Release:        1%{?dist}
Summary:        An Open-Source Free Cross-platform Multi-protocol VPN Program

Group:          Applications/Internet
License:        GPLv2
URL:            http://www.softether.org/
Source0:        http://www.softether-download.com/files/softether/v%{majorversion}.%{minorversion}-%{buildversion}-%{buildrelease}-%{dateversion}-tree/Source_Code/softether-src-v%{majorversion}.%{minorversion}-%{buildversion}-%{buildrelease}.tar.gz

BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(systemd)

%{?systemd_requires}

%description
SoftEther VPN is one of the world's most powerful and easy-to-use multi-protocol VPN software. It runs on Windows, Linux, Mac, FreeBSD, and Solaris.

%package cmd
License:       GPLv2
Summary:       Command line tool for controlling SoftEtherVPN instance
Group:         Applications/Internet

%description cmd
SoftEther VPN is one of the world's most powerful and easy-to-use multi-protocol VPN software.
The %{name}-vpncmd package contains command line tools that can be used
to query, control and configure the VPN server from the console.


%package server
License:       GPLv2
Summary:       The server part of the SoftEtherVPN.
Group:         Applications/Internet
Requires:      %{name}-cmd

%description server
SoftEther VPN is one of the world's most powerful and easy-to-use multi-protocol VPN software.
The %{name}-server package contains the server part.


%package client
License:       GPLv2
Summary:       The client part of the SoftEtherVPN.
Group:         Applications/Internet
Requires:      %{name}-cmd

%description client
SoftEther VPN is one of the world's most powerful and easy-to-use multi-protocol VPN software.
The %{name}-client package contains the server part.


%package bridge
License:       GPLv2
Summary:       The bridge part of the SoftEtherVPN.
Group:         Applications/Internet

%description bridge
SoftEther VPN is one of the world's most powerful and easy-to-use multi-protocol VPN software.
The %{name}-bridge package contains the bridge part.


%prep
%setup -q -n v%{majorversion}.%{minorversion}-%{buildversion}
sed -e 's/\/opt\//\/usr\//g' systemd/softether-vpnserver.service > systemd/softether-vpnserver.service.new
sed -e 's/\/opt\//\/usr\//g' systemd/softether-vpnbridge.service > systemd/softether-vpnbridge.service.new
sed -e 's/\/opt\//\/usr\//g' systemd/softether-vpnclient.service > systemd/softether-vpnclient.service.new

%build
%ifarch i386 i686
cp centos/SOURCES/linux_32bit.mak Makefile
%else
cp centos/SOURCES/linux_64bit.mak Makefile
%endif
make DEBUG=YES

%install
#rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_unitdir}
install -m 755 centos/SOURCES/scripts/vpnserver %{buildroot}%{_bindir}/vpnserver
install -m 755 centos/SOURCES/scripts/vpnbridge %{buildroot}%{_bindir}/vpnbridge
install -m 755 centos/SOURCES/scripts/vpnclient %{buildroot}%{_bindir}/vpnclient
install -m 755 centos/SOURCES/scripts/vpncmd %{buildroot}%{_bindir}/vpncmd
install -m 644 systemd/softether-vpnserver.service.new %{buildroot}%{_unitdir}/softether-vpnserver.service
install -m 644 systemd/softether-vpnbridge.service.new %{buildroot}%{_unitdir}/softether-vpnbridge.service
install -m 644 systemd/softether-vpnclient.service.new %{buildroot}%{_unitdir}/softether-vpnclient.service

%clean
rm -rf $RPM_BUILD_ROOT

%preun server
if [ $1 -eq 0 ]; then
        systemctl stop softether-vpnserver
        systemctl disable softether-vpnserver
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS.TXT BUILD_UNIX.TXT BUILD_WINDOWS.TXT ChangeLog ChangeLog.txt LICENSE LICENSE.TXT README README.TXT THIRD_PARTY.TXT WARNING.TXT

%files cmd
%{_bindir}/vpncmd
%{_usr}/vpncmd/hamcore.se2
%{_usr}/vpncmd/vpncmd

%files server
%{_bindir}/vpnserver
%{_usr}/vpnserver/hamcore.se2
%{_usr}/vpnserver/vpnserver
%{_unitdir}/softether-vpnserver.service

%files client
%{_bindir}/vpnclient
%{_usr}/vpnclient/hamcore.se2
%{_usr}/vpnclient/vpnclient
%{_unitdir}/softether-vpnclient.service

%files bridge
%{_bindir}/vpnbridge
%{_usr}/vpnbridge/hamcore.se2
%{_usr}/vpnbridge/vpnbridge
%{_unitdir}/softether-vpnbridge.service


%changelog
* Wed Dec 22 2021 Max P <skip@email.com> - 4.38.9760-1
- Update upstream to 4.38.9760-rtm
- Split to the subpackages

* Wed Sep 30 2015 Jeff Tang <mrjefftang@gmail.com> - 4.19.9582-1
- Update upstream to 4.19.9582-beta

* Wed Sep 30 2015 Jeff Tang <mrjefftang@gmail.com> - 4.19.9577-1
- Update upstream to 4.19.9577

* Wed Jan 29 2014 Dexter Ang <thepoch@gmail.com> - 4.04.9412-2
- Made initscript more Fedora/RH-like.
- initscript currently using killall. Need to fix this.

* Tue Jan 21 2014 Dexter Ang <thepoch@gmail.com>
- Initial release
