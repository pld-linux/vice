# TODO
# - fonts-TTF-CBM subpackage:
#   %{_fontsdir}/TTF/CBM.ttf
#
# Conditional build:
%bcond_without	pulseaudio	# pulseaudio support
#
Summary:	Versatile Commodore Emulator
Summary(pl.UTF-8):	Uniwersalny emulator Commodore
Name:		vice
Version:	3.3
Release:	2
License:	GPL v2+
Group:		Applications/Emulators
Source0:	http://www.zimmers.net/anonftp/pub/cbm/crossplatform/emulators/VICE/%{name}-%{version}.tar.gz
# Source0-md5:	b0797f534b33f638220418207d606cf5
Source1:	%{name}-c128.desktop
Source2:	%{name}-c64.desktop
Source3:	%{name}-cbm2.desktop
Source4:	%{name}-pet.desktop
Source5:	%{name}-plus4.desktop
Source6:	%{name}-vic20.desktop
Patch0:		%{name}-info.patch
Patch1:		%{name}-fonts.patch
URL:		http://vice-emu.sourceforge.net/
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	ffmpeg-devel
BuildRequires:	flac-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	giflib-devel
BuildRequires:	gtk+3-devel
BuildRequires:	gtkglext-devel
BuildRequires:	lame-libs-devel
BuildRequires:	libieee1284-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmpg123-devel
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libvorbis-devel
BuildRequires:	linux-libc-headers
BuildRequires:	perl-base
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	readline-devel
BuildRequires:	texinfo
BuildRequires:	vte-devel
BuildRequires:	xa
BuildRequires:	xorg-app-bdftopcf
BuildRequires:	xorg-app-mkfontdir
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libXxf86dga-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
Requires(post,postun):	fontpostinst >= 0.1-6
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%{__perl} -i -pe 's@\$\(VICEDIR\)/fonts@%{_fontsdir}/misc@' data/fonts/Makefile.am

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd src/resid
%{__autoconf}
cd ../..
%configure \
	DOS2UNIX=/usr/bin/dos2unix \
	--libdir=%{_datadir} \
	%{?with_pulseaudio:--with-pulse} \
	--enable-libieee1284 \
	--enable-native-gtk3ui \
	--with-sdlsound \
	--enable-external-ffmpeg \
	--enable-ethernet \
	--with-x

# contains some C++ code included as "old" library (.a), so libtool can't detect it
%{__make} \
	CCLD="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__perl} -i -pe 's/SUBDIRS = html\n//' doc/Makefile
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	VICEDIR="%{_datadir}/%{name}"

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/vice/doc
# ?
#ln -sf %{_docdir}/%{name}-%{version}/html $RPM_BUILD_ROOT%{_datadir}/vice/doc

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE6} $RPM_BUILD_ROOT%{_desktopdir}

install -d $RPM_BUILD_ROOT%{_fontsdir}/TTF
mv $RPM_BUILD_ROOT%{_fontsdir}/{misc,TTF}/CBM.ttf

%clean
rm -rf $RPM_BUILD_ROOT

%post
fontpostinst TTF
fontpostinst misc
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
fontpostinst TTF
fontpostinst misc
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FEEDBACK NEWS README doc/iec-bus.txt doc/html
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
%{_fontsdir}/misc/vice-cbm.bdf
%{_fontsdir}/TTF/CBM.ttf
%{_mandir}/man1/cartconv.1*
%{_mandir}/man1/c1541.1*
%{_mandir}/man1/petcat.1*
%{_mandir}/man1/vice.1*
%{_infodir}/vice.info*
%{_desktopdir}/vice-*.desktop
