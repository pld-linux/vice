#
# Conditional build:
# _without_gnome - without GNOME support
#
Summary:	Commodore emulator
Summary(pl):	Emulator Commodore
Name:		vice
Version:	1.8
Release:	1
License:	GPL
Group:		Applications/Emulators
Source0:	ftp://ftp.funet.fi/pub/cbm/crossplatform/emulators/VICE/%{name}-%{version}.tar.gz
Patch0:		%{name}-info.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-acamfixes.patch
URL:		http://viceteam.bei.t-online.de/
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	XFree86-devel
BuildRequires:	Xaw3d-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	esound-devel
BuildRequires:	flex
BuildRequires:	gettext-devel
%{!?_without_gnome:BuildRequires:	gnome-libs-devel}
BuildRequires:	libpng-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

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
#%patch2 -p1

%build
rm -f missing
%{__gettextize}
#aclocal
#autoconf
#autoheader
#automake -a -c -f
#cd src/resid
#autoconf
#cd ../..
if [ -f %{_pkgconfigdir}/libpng12.pc ] ; then
	CPPFLAGS="`pkg-config libpng12 --cflags`"; export CPPFLAGS
fi
%configure2_13 \
	--enable-autobpp \
	--with-sdl \
	--with-x \
	--enable-fullscreen \
	--without-xaw3d \
	%{!?_without_gnome:--enable-gnomeui} \
	--enable-nls \
	--without-included-gettext
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf AUTHORS  Chan* FEEDBACK NEWS README 

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(0755,root,root) %{_bindir}/*
%{_libdir}/vice
%{_mandir}/man?/*
%{_infodir}/*.info*
