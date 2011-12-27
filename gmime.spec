#
# Conditional build:
%bcond_without	dotnet	# without .NET support
#
%ifarch i386
%undefine	with_dotnet
%endif
%{?with_dotnet:%include	/usr/lib/rpm/macros.mono}
Summary:	GMIME library
Summary(pl.UTF-8):	Biblioteka GMIME
Name:		gmime
Version:	2.6.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gmime/2.6/%{name}-%{version}.tar.xz
# Source0-md5:	db9d8e40c2b3f969aca28f56c4ea1803
Patch0:		%{name}-link.patch
URL:		http://spruce.sourceforge.net/gmime/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.18.0
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

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-largefile \
	--%{?with_dotnet:enable}%{!?with_dotnet:disable}-mono \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

# packaged in sharutils
%{__rm} $RPM_BUILD_ROOT%{_bindir}/uu{de,en}code
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

%files devel
%defattr(644,root,root,755)
%doc PORTING
%attr(755,root,root) %{_libdir}/libgmime-2.6.so
%{_pkgconfigdir}/gmime-2.6.pc
%{_includedir}/gmime-2.6

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
%{_pkgconfigdir}/gmime-sharp-2.6.pc
%endif
