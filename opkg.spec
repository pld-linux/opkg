#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	pathfinder	# PathFinder certificate verification support
#
Summary:	OPKG Package Management System (designed for OpenMoko)
Summary(pl.UTF-8):	System zarządzania pakietami OPKG (zaprojektowany dla OpenMoko)
Name:		opkg
Version:	0.2.0
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://code.google.com/p/opkg/downloads/list
Source0:	https://opkg.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	e8a6fd34fb2529191fe09dc14c934cc3
Patch0:		%{name}-libdir.patch
URL:		https://code.google.com/p/opkg/
BuildRequires:	curl-devel
BuildRequires:	gpgme-devel >= 1.0.0
BuildRequires:	pkgconfig >= 1:0.20
%if %{with pathfinder}
BuildRequires:	dbus-devel >= 1
BuildRequires:	openssl-devel
BuildRequires:	pathfinder-openssl-devel
%endif
Requires:	gpgme >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OPKG Package Management System (designed for OpenMoko).

%description -l pl.UTF-8
System zarządzania pakietami OPKG (zaprojektowany dla OpenMoko).

%package devel
Summary:	Header files for OPKG library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OPKG
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OPKG library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OPKG.

%package static
Summary:	Static OPKG library
Summary(pl.UTF-8):	Statyczna biblioteka OPKG
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OPKG library.

%description static -l pl.UTF-8
Statyczna biblioteka OPKG.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-shave \
	%{!?with_static_libs:--disable-static} \
	%{?with_pathfinder:--enable-pathfinder} \
	--enable-sha256 \
	--with-opkgetcdir=%{_sysconfdir} \
	--with-opkglibdir=/var/lib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/lib/opkg,%{_sysconfdir}/opkg}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/update-alternatives
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libopkg.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTORS ChangeLog* NEWS README TODO
%attr(755,root,root) %{_bindir}/opkg-cl
%attr(755,root,root) %{_bindir}/opkg-key
%attr(755,root,root) %{_libdir}/libopkg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopkg.so.1
%dir %{_sysconfdir}/opkg
%dir %{_datadir}/opkg
%dir %{_datadir}/opkg/intercept
%attr(755,root,root) %{_datadir}/opkg/intercept/*
%dir /var/lib/opkg
%{_mandir}/man1/opkg-cl.1*
%{_mandir}/man1/opkg-key.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopkg.so
%{_includedir}/libopkg
%{_pkgconfigdir}/libopkg.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libopkg.a
%endif
