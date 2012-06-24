Summary:	libGMIME library
Summary(pl):	Biblioteka GMIME
Name:		gmime
Version:	2.1.0
Release:	1
License:	LGPL
Group:		Development/Libraries
Source0:	http://spruce.sourceforge.net/gmime/sources/gmime-%{version}.tar.gz
# Source0-md5:	dba1e7c39b3a7274c485aa81069b5edf
Patch0:		%{name}-link.patch
Patch1:		%{name}-ipv6-fix.patch
URL:		http://spruce.sourceforge.net/gmime/
BuildRequires:	autoconf
BuildRequires:	automake
# glib2-devel is needed for aclocal/autoconf call (m4 macros) and to build test programs
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows you to manipulate MIME messages.

%description -l pl
Ta biblioteka pozwala na manipulowanie wiadomo�ciami MIME.

%package devel
Summary:	Libraries, includes, etc to develop libgmime applications
Summary(pl):	Biblioteki, nag��wki, itp. do tworzenia program�w z libgmime
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	gtk-doc-common

%description devel
Libraries, include files, etc you can use to develop libgmime
applications.

%description devel -l pl
Bibliotek, pliki nag��wkowe itp. potrzebne do tworzenia program�w
opartych o bibliotek� gmime.

%package static
Summary:	Static gmime libraries
Summary(pl):	Statyczne biblioteki gmime
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static gmime libraries.

%description static -l pl
Statyczne biblioteki gmime.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-ipv6 \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gmime-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/*.sh
%{_pkgconfigdir}/*.pc
%{_includedir}/gmime-2.0
%{_gtkdocdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
