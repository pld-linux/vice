Summary:	Commodore emulator
Summary(pl):	Emulator Commodore
Name:		vice
Version:	1.6
Release:	1
License:	GPL
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Source0:	ftp://ftp.funet.fi/pub/cbm/crossplatform/emulators/VICE/%{name}-%{version}.tar.gz
Patch0:		%{name}-info.patch
URL:		http://www.cs.cmu.edu/~dsladic/vice/vice.html
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	XFree86-devel
BuildRequires:	Xaw3d-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	esound-devel
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel
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

%build
rm missing
gettextize --copy --force
aclocal
autoconf
autoheader
automake -a -c
%configure \
	--enable-autobpp \
	--with-sdl \
	--with-x \
	--enable-fullscreen \
	--without-xaw3d \
	--enable-gnomeui \
	--enable-nls \
	--without-included-gettext
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf AUTHORS BUGS Chan* FEEDBACK NEWS README TODO

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(0755,root,root) %{_bindir}/*
%{_libdir}/vice
%{_mandir}/man?/*
%{_infodir}/*info*
