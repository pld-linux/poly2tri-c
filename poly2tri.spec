Name:		poly2tri
Version:	0.0
%global         date 20150515
%global         snapshot %{date}hg%{rev}
Summary:	A 2D constrained Delaunay triangulation library
Release:	0.%{date}.1
License:	BSD
Group:		Development/Libraries
URL:		https://code.google.com/p/poly2tri
Source0:	https://poly2tri-c.googlecode.com/archive/5ac75d6f09e4de35ef33289c69bc1d46c2a04970.tar.gz
# Source0-md5:	844558199746106bd76043b716c10c85
Patch0:		%{name}-build.patch
BuildRequires:	Mesa-libGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool

%description
Library based on the paper "Sweep-line algorithm for constrained
Delaunay triangulation" by V. Domiter and and B. Zalik.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%setup -q -n %{name}-c-5ac75d6f09e4
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

%configure \
	--disable-silent-rules
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/lib%{name}-c-*.{a,la}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/p2tc
%attr(755,root,root) %ghost %{_libdir}/lib%{name}-c-*.so.0
%attr(755,root,root) %{_libdir}/lib%{name}-c-*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}-c-*.so
%{_includedir}/%{name}-c-*
%{_pkgconfigdir}/poly2tri-c.pc
