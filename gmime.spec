# NOTE: for gmime 3.0.x see gmime3.spec
#
# Conditional build:
%bcond_without	dotnet	# without .NET support

%ifarch i386 x32
%undefine	with_dotnet
%endif

%{?with_dotnet:%include	/usr/lib/rpm/macros.mono}
Summary:	GMIME library
Summary(pl.UTF-8):	Biblioteka GMIME
Name:		gmime
Version:	2.6.23
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gmime/2.6/%{name}-%{version}.tar.xz
# Source0-md5:	247072236d84bd0fbbff299d69bdf333
Patch0:		%{name}-link.patch
Patch1:		%{name}-am.patch
URL:		http://spruce.sourceforge.net/gmime/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gpgme-devel >= 1:1.1.6
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
%if %{with dotnet}
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.9.0
BuildRequires:	mono-csharp >= 1.1.16.1
%endif
Requires:	glib2 >= 1:2.18.0
Requires:	gpgme >= 1:1.1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows you to manipulate MIME messages.

%description -l pl.UTF-8
Ta biblioteka pozwala na manipulowanie wiadomościami MIME.

%package devel
Summary:	Header files to develop libgmime applications
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów z użyciem libgmime
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.18.0
Requires:	gpgme-devel >= 1:1.1.6
Requires:	zlib-devel

%description devel
Header files develop libgmime applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia programów z użyciem libgmime.

%package static
Summary:	Static gmime library
Summary(pl.UTF-8):	Statyczna biblioteka gmime
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gmime library.

%description static -l pl.UTF-8
Statyczna biblioteka gmime.

%package apidocs
Summary:	gmime library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki gmime
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
gmime library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gmime.

%package -n dotnet-gmime-sharp
Summary:	.NET language bindings for gmime
Summary(pl.UTF-8):	Wiązania gmime dla .NET
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dotnet-gtk-sharp2 >= 2.9.0
Requires:	mono >= 1.1.16.1

%description -n dotnet-gmime-sharp
.NET language bindings for gmime

%description -n dotnet-gmime-sharp -l pl.UTF-8
Wiązania gmime dla .NET

%package -n dotnet-gmime-sharp-devel
Summary:	Development part of dotnet-gmime-sharp
Summary(pl.UTF-8):	Część dla programistów dotnet-gmime-sharp
Group:		Development/Libraries
Requires:	dotnet-%{name}-sharp = %{version}-%{release}

%description -n dotnet-gmime-sharp-devel
Development part of dotnet-gmime-sharp.

%description -n dotnet-gmime-sharp-devel -l pl.UTF-8
Część dla programistów dotnet-gmime-sharp.

%package -n vala-gmime
Summary:	Vala API for gmime library
Summary(pl.UTF-8):	API języka Vala do biblioteki gmime
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-gmime
Vala API for gmime library.

%description -n vala-gmime -l pl.UTF-8
API języka Vala do biblioteki gmime.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-largefile \
	--enable-mono%{!?with_dotnet:=no} \
	--disable-silent-rules \
	--enable-smime \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgmime-2.6.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/libgmime-2.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgmime-2.6.so.0
%{_libdir}/girepository-1.0/GMime-2.6.typelib

%files devel
%defattr(644,root,root,755)
%doc PORTING
%attr(755,root,root) %{_libdir}/libgmime-2.6.so
%{_includedir}/gmime-2.6
%{_datadir}/gir-1.0/GMime-2.6.gir
%{_pkgconfigdir}/gmime-2.6.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgmime-2.6.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gmime-2.6

%if %{with dotnet}
%files -n dotnet-gmime-sharp
%defattr(644,root,root,755)
%{_prefix}/lib/mono/gac/gmime-sharp

%files -n dotnet-gmime-sharp-devel
%defattr(644,root,root,755)
%{_prefix}/lib/mono/gmime-sharp-2.6
%{_datadir}/gapi-2.0/gmime-api.xml
%{_pkgconfigdir}/gmime-sharp-2.6.pc
%endif

%files -n vala-gmime
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gmime-2.6.deps
%{_datadir}/vala/vapi/gmime-2.6.vapi
