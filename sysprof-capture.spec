# Static archive only. find-debuginfo writes an empty debugsource list
# and rpmbuild then refuses to package it.
%global _enable_debug_packages 0

Name:		sysprof-capture
Version:	51.0
Release:	1
Summary:	Static Sysprof capture library
License:	BSD-2-Clause
Group:		System/Libraries
URL:		https://www.sysprof.com
Source0:	https://download.gnome.org/sources/sysprof/51/sysprof-%{version}.tar.xz

# glib-devel needs pkgconfig(sysprof-capture-4). The full sysprof devel
# package also needs libdex, which still requires Python 3.14, so a
# capture-only build is what lets glib-devel be installed.
BuildRequires:	meson
BuildRequires:	ninja
BuildRequires:	gettext

# Do not install this next to the full devel package. Both ship the
# capture library and the pkgconfig file.
Conflicts:	%{mklibname sysprof -d}

%description
libsysprof-capture is the static library GLib and other low-level
components use to emit Sysprof marks. It does not depend on libdex or
the Sysprof UI.

%prep
%autosetup -n sysprof-%{version} -p1

%build
%meson \
	-Dgtk=false \
	-Dlibsysprof=false \
	-Dtools=false \
	-Dtests=false \
	-Dexamples=false \
	-Dsysprofd=none \
	-Dhelp=false \
	-Dinstall-static=true \
	-Dintrospection=disabled \
	-Ddocs=false \
	-Ddebuginfod=disabled \
	-Dpolkit-agent=disabled
%meson_build

%install
%meson_install

%files
%license src/libsysprof-capture/COPYING
%{_includedir}/sysprof-6/
%{_libdir}/libsysprof-capture-4.a
%{_libdir}/pkgconfig/sysprof-capture-4.pc
