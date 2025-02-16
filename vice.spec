#
# Conditional build:
%bcond_without	ieee1284	# IEEE 1284 (parallel port) support for ParSID
%bcond_without	openmp		# OpenMP support
%bcond_without	pulseaudio	# pulseaudio support
%bcond_with	catweasel	# CatWeasel MK3 (PCI) hardware SID support
%bcond_with	ffmpeg		# FFmpeg support
%bcond_with	hardsid		# HardSID (ISA/PCI) hardware SID support
%bcond_with	parsid		# ParSID (IEEE1284) hardware SID support
%bcond_with	ssi2001		# SSI2001 (ISA) hardware SID support
#
%if %{without parsid}
%undefine	with_ieee1284
%endif
Summary:	Versatile Commodore Emulator
Summary(pl.UTF-8):	Uniwersalny emulator Commodore
Name:		vice
Version:	3.7.1
Release:	2
License:	GPL v2+
Group:		Applications/Emulators
Source0:	https://downloads.sourceforge.net/vice-emu/%{name}-%{version}.tar.gz
# Source0-md5:	ffcb48e9b688d14dc5f86de22c30ee32
Source1:	%{name}-c128.desktop
Source2:	%{name}-c64.desktop
Source3:	%{name}-cbm2.desktop
Source4:	%{name}-pet.desktop
Source5:	%{name}-plus4.desktop
Source6:	%{name}-vic20.desktop
Patch0:		%{name}-info.patch
Patch1:		%{name}-bash.patch
Patch2:		%{name}-opt.patch
Patch3:		%{name}-link.patch
URL:		https://vice-emu.sourceforge.io/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	SDL2-devel >= 2.0
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel < 5}
BuildRequires:	flac-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel >= 2.0.0
BuildRequires:	giflib-devel
BuildRequires:	glew-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	lame-libs-devel
%{?with_ieee1284:BuildRequires:	libieee1284-devel}
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	libmpg123-devel
BuildRequires:	libogg-devel
BuildRequires:	libpcap-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libvorbis-devel
BuildRequires:	linux-libc-headers
%if %{with catweasel} || %{with hardsid}
BuildRequires:	pciutils-devel
%endif
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	texinfo
BuildRequires:	xa
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
Requires:	fontconfig >= 2.0.0
Requires:	gtk+3 >= 3.22
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VICE is a Versatile Commodore Emulator, i.e. a program that runs on a
Unix, MS-DOS, Win95/NT, OS/2, RiscOS or BeOS machine and executes
programs intended for the old 8-bit Commodore computers. The current
version emulates the C64, the C128 (80 column screen is included now),
the VIC20, all the PET models (except the SuperPET 9000, which is out
of line anyway), CBM-II (aka C610) and the Plus4.

%description -l pl.UTF-8
VICE jest wszechstronnym emulatorem 8-bitowego komputera Commodore.
Aktualna wersja emuluje C64, C128 (wraz z trybem pracy 80 kolumnowym),
VIC20, wszystkie modele PET (poza SuperPET 9000, który zresztą nie
pasował do tej linii), CBM-II (C610) oraz Plus4.

%package doc
Summary:	VICE documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do VICE w formacie HTML
Group:		Documentation
BuildArch:	noarch

%description doc
VICE documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do VICE w formacie HTML.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
export CFLAGS="%{rpmcflags} -fcommon"
%configure \
	DOS2UNIX=/usr/bin/dos2unix \
	%{?with_catweasel:--enable-catweasel} \
	--enable-ethernet \
	%{__enable_disable ffmpeg} \
	--enable-gtk3ui \
	%{!?with_hardsid:--disable-hardsid} \
	--enable-lame \
	%{?with_ieee1284:--enable-libieee1284} \
	--enable-midi \
	%{!?with_openmp:--disable-openmp} \
	%{?with_parsid:--enable-parsid} \
	--disable-pdf-docs \
	%{?with_ssi2001:--enable-ssi2001} \
	--enable-x64 \
	--enable-x64-image \
	--with-flac \
	--with-libcurl \
	--with-mpg123 \
	--with-oss \
	%{?with_pulseaudio:--with-pulse} \
	--with-sdlsound \
	--with-vorbis

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{_desktopdir}

%{__rm} $RPM_BUILD_ROOT%{_docdir}/vice/{*.txt,*.md,vice.texi}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc NEWS README doc/{CIA-README.txt,iec-bus.txt,readmes/Readme-SDL2.txt} doc/html/fonts/OFL.txt
%attr(755,root,root) %{_bindir}/c1541
%attr(755,root,root) %{_bindir}/cartconv
%attr(755,root,root) %{_bindir}/petcat
%attr(755,root,root) %{_bindir}/vsid
%attr(755,root,root) %{_bindir}/x128
%attr(755,root,root) %{_bindir}/x64
%attr(755,root,root) %{_bindir}/x64dtv
%attr(755,root,root) %{_bindir}/x64sc
%attr(755,root,root) %{_bindir}/xcbm2
%attr(755,root,root) %{_bindir}/xcbm5x0
%attr(755,root,root) %{_bindir}/xpet
%attr(755,root,root) %{_bindir}/xplus4
%attr(755,root,root) %{_bindir}/xscpu64
%attr(755,root,root) %{_bindir}/xvic
%{_datadir}/vice
%{_infodir}/vice.info*
%{_desktopdir}/vice-*.desktop

%files doc
%defattr(644,root,root,755)
%doc doc/html/{fonts,images,*.css,*.html,NEWS,COPYING,favicon.ico,robots.txt}
