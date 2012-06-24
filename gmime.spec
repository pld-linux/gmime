# Note that this is NOT a relocatable package
%define ver      0.1.0
%define prefix   /usr

Summary: libGMIME library
Name: libgmime
Version: %ver
Release: 1
Copyright: LGPL
Group: Development/Libraries
Source: ftp://ftp.gnome.org/pub/GNOME/sources/libgmime/libgmime-%{ver}.tar.gz
BuildRoot: /var/tmp/libgmime-%{PACKAGE_VERSION}-root

URL: http://primates.helixcode.com/~fejj/GMIME/
Prereq: /sbin/install-info
Docdir: %{prefix}/doc

%description
This library allows you to manipulate MIME messages.

%package devel
Summary: Libraries, includes, etc to develop libgmime applications
Group: Development/Libraries
Requires: libgmime = %{version}

%description devel
Libraries, include files, etc you can use to develop libgmime applications.


%changelog

- Built release 0.1.0

%prep
%setup

%build
# Needed for snapshot releases.
if [ ! -f configure ]; then
%ifarch alpha
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --host=alpha-redhat-linux --prefix=%prefix --sysconfdir="/etc"
%else
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=%prefix --sysconfdir="/etc"
%endif
else
%ifarch alpha
  CFLAGS="$RPM_OPT_FLAGS" ./configure --host=alpha-redhat-linux --prefix=%prefix --sysconfdir="/etc"
%else
  CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%prefix --sysconfdir="/etc"
%endif
fi

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make
else
  make
fi

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{prefix} install
#
# hack to get libgmime.so.0 too !
# Get rid of it once deps to libgmime.so.0 have disapeared.
#
#if [ -f $RPM_BUILD_ROOT/%{prefix}/lib/libgmime.so.0.1.0 ]
#then
#   (cd $RPM_BUILD_ROOT/%{prefix}/lib/ ; cp libgmime.so.0.1.0 libgmime.so.0.99.0 ; ln -sf libgmime.so.0.99.0 libgmime.so.0)
#fi
#
# another hack to get /usr/include/gnome-gmime/libgmime/
#
if [ -d $RPM_BUILD_ROOT/%{prefix}/include/gnome-gmime ]
then
    (cd $RPM_BUILD_ROOT/%{prefix}/include/gnome-gmime ; ln -sf . libgmime)
fi

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)

%doc AUTHORS ChangeLog NEWS README COPYING COPYING.LIB TODO
%{prefix}/lib/lib*.so.*

%files devel
%defattr(-, root, root)

%{prefix}/lib/lib*.so
%{prefix}/lib/*a
%{prefix}/lib/*.sh
%{prefix}/include/*
%{prefix}/bin/gmime-config
