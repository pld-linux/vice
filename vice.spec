Summary:	Versatile Commodore Emulator
Summary(pl.UTF-8):	Uniwersalny emulator Commodore
Name:		vice
Version:	2.1
Release:	3
License:	GPL v2+
Group:		Applications/Emulators
Source0:	http://www.zimmers.net/anonftp/pub/cbm/crossplatform/emulators/VICE/%{name}-%{version}.tar.gz
# Source0-md5:	a4cca1aad12e12ac7f37d6c85310ade8
Source1:	%{name}-c128.desktop
Source2:	%{name}-c64.desktop
Source3:	%{name}-cbm2.desktop
Source4:	%{name}-pet.desktop
Source5:	%{name}-plus4.desktop
Source6:	%{name}-vic20.desktop
Patch0:		%{name}-info.patch
Patch1:		%{name}-gettext.patch
Patch2:		%{name}-home_etc.patch
Patch3:		%{name}-gcc44.patch
URL:		http://www.viceteam.org/
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	esound-devel
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	giflib-devel
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	lame-libs-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	texinfo
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
%patch2 -p1
%patch3 -p1
%{__perl} -i -pe 's@\$\(VICEDIR\)/fonts@%{_fontsdir}/misc@' data/fonts/Makefile.am

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
	--enable-gnomeui \
	--enable-nls \
	--without-xaw3d \
	--without-included-gettext \
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

rm -f doc/html/{Makefile*,texi2html}
rm -rf $RPM_BUILD_ROOT%{_datadir}/vice/doc
# ?
#ln -sf %{_docdir}/%{name}-%{version}/html $RPM_BUILD_ROOT%{_datadir}/vice/doc

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE6} $RPM_BUILD_ROOT%{_desktopdir}

cd src/arch/unix/x11
for i in *icon.c; do
	install $i $RPM_BUILD_ROOT%{_pixmapsdir}/${i%.c}.xpm
done
cd ../../../..

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
%attr(755,root,root) %{_bindir}/*
%{_datadir}/vice
%{_fontsdir}/misc/*
%{_mandir}/man?/*
%{_infodir}/*.info*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
