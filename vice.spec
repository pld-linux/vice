#
# Conditional build:
%bcond_without	gnome	# without GNOME support
#
Summary:	Commodore emulator
Summary(pl):	Emulator Commodore
Name:		vice
Version:	1.16
Release:	1
License:	GPL
Group:		Applications/Emulators
Source0:	ftp://ftp.funet.fi/pub/cbm/crossplatform/emulators/VICE/%{name}-%{version}.tar.gz
# Source0-md5:	23848e7fe588b32549a5ce4ccf056207
Patch0:		%{name}-info.patch
Patch1:		%{name}-FHS.patch
Patch2:		%{name}-gettext.patch
Patch3:		%{name}-home_etc.patch
URL:		http://www.viceteam.org/
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	esound-devel
BuildRequires:	flex
BuildRequires:	gettext-devel
%{?with_gnome:BuildRequires:	gnome-libs-devel}
BuildRequires:	libpng-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
Requires(post,postun):	fontpostinst >= 0.1-6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VICE is a Versatile Commodore Emulator, i.e. a program that runs on a
Unix, MS-DOS, Win95/NT, OS/2, RiscOS or BeOS machine and executes
programs intended for the old 8-bit Commodore computers. The current
version emulates the C64, the C128 (80 column screen is included now),
the VIC20, all the PET models (except the SuperPET 9000, which is out
of line anyway) and the CBM-II (aka C610).

%description -l pl
VICE jest wszechstronnym emulatorem 8-bitowego komputera Commodore.
Aktualna wersja emuluje C64, C128 (wraz z trybem pracy 80 kolumnowym),
VIC20, wszystkie modele PET (poza SuperPET 9000) oraz CBM-II (C610).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd src/resid
%{__autoconf}
cd ../..
%configure \
	--libdir=%{_datadir} \
	--enable-autobpp \
	--with-sdl \
	--enable-fullscreen \
	%{?with_gnome:--enable-gnomeui} \
	--enable-nls \
	--without-xaw3d \
	--without-included-gettext \
	--with-x
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

perl -i -pe 's/SUBDIRS = html\n//' doc/Makefile
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9 $RPM_BUILD_ROOT%{_fontsdir}/misc/*
rm -f doc/html/{Makefile*,texi2html}
rm -rf $RPM_BUILD_ROOT%{_datadir}/vice/doc
ln -sf %{_docdir}/%{name}-%{version}/html $RPM_BUILD_ROOT%{_datadir}/vice/doc

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
fontpostinst misc
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
fontpostinst misc
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FEEDBACK NEWS README doc/iec-bus.txt doc/mon.txt doc/html
%attr(0755,root,root) %{_bindir}/*
%{_datadir}/vice
%{_fontsdir}/misc/*
%{_mandir}/man?/*
%{_infodir}/*.info*
