%define major 12
%define libname %mklibname flac 12

%define majorpp 10
%define libnamepp %mklibname flac++ 10
%global optflags %{optflags} -O3

%define lib32name libflac12
%define lib32namepp libflac++10

# flac is used by audiofile, which is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

Summary:	An encoder/decoder for the Free Lossless Audio Codec
Name:		flac12
Version:	1.4.3
Release:	1
License:	BSD and GPLv2+
Group:		Sound
Url:		https://flac.sourceforge.net/
Source0:	https://downloads.xiph.org/releases/flac/flac-%{version}.tar.xz
Patch0:		flac-1.3.3-no-Lusrlib.patch
BuildRequires:	libtool
%ifarch %{ix86}
BuildRequires:	nasm
%endif
BuildRequires:	gettext-devel
BuildRequires:	id3lib-devel
BuildRequires:	pkgconfig(ogg)
BuildRequires:	doxygen
%if %{with compat32}
BuildRequires:	devel(libogg)
%endif

%description
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

FLAC is comprised of 1) `libFLAC', a library which implements
reference encoders and decoders, licensed under the GNU Lesser
General Public License (LGPL); 2) `flac', a command-line program for
encoding and decoding files, licensed under the GNU General public
License (GPL); 3) `metaflac', a command-line program for editing
FLAC metadata, licensed under the GPL; 4) player plugins for XMMS
and Winamp, licensed under the GPL; and 5) documentation, licensed
under the GNU Free Documentation License.

%package -n %{libname}
Summary:	Shared libraries for FLAC
Group:		System/Libraries

%description  -n %{libname}
This package contains the C libraries.

%package -n %{libnamepp}
Summary:	Shared C++ libraries for FLAC
Group:		System/Libraries

%description  -n %{libnamepp}
This package contains the libraries for C++ applications.

%package -n %{lib32name}
Summary:	Shared libraries for FLAC (32-bit)
Group:		System/Libraries

%description  -n %{lib32name}
This package contains the C libraries.

%package -n %{lib32namepp}
Summary:	Shared C++ libraries for FLAC (32-bit)
Group:		System/Libraries

%description  -n %{lib32namepp}
This package contains the libraries for C++ applications.

%prep
export LC_ALL=C.utf-8
%autosetup -p1 -n flac-%{version}
./autogen.sh -V
autoreconf -fi

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32
cd ..
unset PKG_CONFIG_PATH
%endif

mkdir buildnative
cd buildnative
%configure \
	--disable-static \
	--disable-xmms-plugin \
	--disable-thorough-tests \
	--enable-asm-optimizations

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C buildnative

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C buildnative

# No development files or applications for compat packages
rm -rf %{buildroot}%{_includedir} \
	%{buildroot}%{_libdir}/*.so \
	%{buildroot}%{_libdir}/pkgconfig \
	%{buildroot}%{_prefix}/lib/*.so \
	%{buildroot}%{_prefix}/lib/pkgconfig \
	%{buildroot}%{_datadir}/aclocal \
	%{buildroot}%{_docdir} \
	%{buildroot}%{_bindir}/flac \
	%{buildroot}%{_bindir}/metaflac \
	%{buildroot}%{_mandir} \

%files -n %{libname}
%{_libdir}/libFLAC.so.%{major}*

%files -n %{libnamepp}
%{_libdir}/libFLAC++.so.%{majorpp}*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libFLAC.so.%{major}*

%files -n %{lib32namepp}
%{_prefix}/lib/libFLAC++.so.%{majorpp}*
%endif
