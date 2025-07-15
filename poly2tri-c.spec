#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	A 2D constrained Delaunay triangulation library
Summary(pl.UTF-8):	Biblioteka triangulacji Delaunaya z ograniczeniami w 2D
Name:		poly2tri-c
Version:	0.0
%define	snap	20150515
Release:	0.%{snap}.1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/KyleLink/poly2tri-c/tags
#Source0:	https://poly2tri-c.googlecode.com/archive/5ac75d6f09e4de35ef33289c69bc1d46c2a04970.tar.gz
Source0:	5ac75d6f09e4de35ef33289c69bc1d46c2a04970.tar.gz
# Source0-md5:	f800bb38025009fefe781841ed0a3c36
Patch0:		%{name}-build.patch
Patch1:		compile.patch
URL:		https://github.com/KyleLink/poly2tri-c
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
Requires:	glib2 >= 1:2.28
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a C port of the poly2tri library - a fast and powerful library
for computing 2D constrained Delaunay triangulations. Instead of the
standard C++ library (which included some utilities and template-based
data structures), this port depends on GLib for it's data structures
and some of it's utilities.

%description -l pl.UTF-8
Ten pakiet zawiera port C biblioteki poly2tri - szybkiej i potężnej
biblioteki do obliczania triangulacji Delaunaya z ograniczeniami w 2D.
Zamiast biblioteki standardowej C++ (zawierającej trochę narzędzi oraz
struktury danych oparte na szablonach), ten port wykorzystuje
bibliotekę GLib na potrzeby struktur danych oraz niektórych narzędzi.

%package devel
Summary:	Development files for poly2tri-c library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki poly2tri-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.28

%description devel
Development files for poly2tri-c library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki poly2tri-c.

%package static
Summary:	Static poly2tri-c library
Summary(pl.UTF-8):	Biblioteka statyczna poly2tri-c
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static poly2tri-c library.

%description static -l pl.UTF-8
Biblioteka statyczna poly2tri-c.

%prep
%setup -q -n %{name}-5ac75d6f09e4
%patch -P0 -p1
%patch -P1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libpoly2tri-c-*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING LICENSE-Poly2Tri.txt LICENSE-Poly2Tri-C.txt README
%attr(755,root,root) %{_bindir}/p2tc
%attr(755,root,root) %{_libdir}/libpoly2tri-c-0.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpoly2tri-c-0.1.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpoly2tri-c-0.1.so
%{_includedir}/poly2tri-c-0.1
%{_pkgconfigdir}/poly2tri-c.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpoly2tri-c-0.1.a
%endif
