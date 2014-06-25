%bcond_with wayland
%bcond_with mobile
%bcond_with rdp

%if %{with mobile}
%define extra_config_options1 --disable-drm-compositor
%endif

%if %{with rdp}
%define extra_config_options2 --enable-rdp-compositor
%endif

%if "%{profile}" == "common"
%define extra_config_options3 --enable-sys-uid
%endif

Name:           weston
Version:        1.5.0
Release:        0
Summary:        Wayland Compositor Infrastructure
License:        MIT
Group:          Graphics & UI Framework/Wayland Window System
Url:            http://weston.freedesktop.org/

#Git-Clone:	git://anongit.freedesktop.org/wayland/weston
#Git-Web:	http://cgit.freedesktop.org/wayland/weston/
Source0:         %name-%version.tar.xz
Source1:        weston.target
Source1001: 	weston.manifest
BuildRequires:	autoconf >= 2.64, automake >= 1.11
BuildRequires:  expat-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtool >= 2.2
BuildRequires:  libvpx-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig
BuildRequires:  xz
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-egl) >= 1.11.3
BuildRequires:  pkgconfig(egl) >= 7.10
%if %{with rdp}
BuildRequires:  pkgconfig(freerdp)
%endif
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libdrm) >= 2.4.30
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libsystemd-login)
BuildRequires:  pkgconfig(libudev) >= 136
BuildRequires:  pkgconfig(mtdev) >= 1.1.0
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xkbcommon) >= 0.3.0
Requires:       weston-startup
Requires(pre):  /usr/sbin/groupadd

%if !%{with wayland}
ExclusiveArch:
%endif

%description
Weston is the reference implementation of a Wayland compositor, and a
useful compositor in its own right. Weston has various backends that
lets it run on Linux kernel modesetting and evdev input as well as
under X11. Weston ships with a few example clients, from simple
clients that demonstrate certain aspects of the protocol to more
complete clients and a simplistic toolkit. There is also a quite
capable terminal emulator (weston-terminal) and an toy/example
desktop shell. Finally, weston also provides integration with the
Xorg server and can pull X clients into the Wayland desktop and act
as a X window manager.

%package devel
Summary: Development files for package %{name}
Group:   Graphics & UI Framework/Development
%description devel
This package provides header files and other developer releated files
for package %{name}.

%package clients
Summary: Sample clients for package %{name}
Group:   Graphics & UI Framework/Development
%description clients
This package provides a set of example wayland clients useful for
validating the functionality of wayland with very little dependencies
on other system components.

%if %{with rdp}
%package rdp
Summary: RDP compositor for %{name}
Group:   Graphics & UI Framework/Development
%description rdp
This package provides a RDP compositor allowing to do remote rendering
through the network.
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
%autogen --disable-static \
         --disable-setuid-install \
         --enable-simple-clients \
         --enable-clients \
         --disable-libunwind \
         --disable-xwayland \
         --disable-xwayland-test \
         --disable-x11-compositor \
         --disable-rpi-compositor \
         %{?extra_config_options1:%extra_config_options1} \
         %{?extra_config_options2:%extra_config_options2} \
         %{?extra_config_options3:%extra_config_options3}

make %{?_smp_mflags}

%install
%make_install

# install example clients
install -m 755 weston-calibrator %{buildroot}%{_bindir}
install -m 755 weston-simple-touch %{buildroot}%{_bindir}
install -m 755 weston-simple-shm %{buildroot}%{_bindir}
install -m 755 weston-simple-egl %{buildroot}%{_bindir}
install -m 755 weston-flower %{buildroot}%{_bindir}
install -m 755 weston-image %{buildroot}%{_bindir}
install -m 755 weston-cliptest %{buildroot}%{_bindir}
install -m 755 weston-dnd %{buildroot}%{_bindir}
install -m 755 weston-editor %{buildroot}%{_bindir}
install -m 755 weston-smoke %{buildroot}%{_bindir}
install -m 755 weston-resizor %{buildroot}%{_bindir}
install -m 755 weston-eventdemo %{buildroot}%{_bindir}
install -m 755 weston-clickdot %{buildroot}%{_bindir}
install -m 755 weston-subsurfaces %{buildroot}%{_bindir}
install -m 755 weston-transformed %{buildroot}%{_bindir}
install -m 755 weston-fullscreen %{buildroot}%{_bindir}


install -d %{buildroot}%{_unitdir_user}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir_user}/weston.target
# The weston.service unit file must be provided by the weston-startup
# virtual package, i.e. "Provide: weston-startup".  The weston-startup
# virtual package requirement is intended to force Tizen profile
# maintainers to add the necessary start-up script or systemd unit
# file to start weston. Otherwise it becomes possible to install
# weston without an automated means to start weston at boot, which may
# lead to confusion.  This approach allows startup related files to be
# maintained outside of this weston package.

%pre
getent group weston-launch >/dev/null || %{_sbindir}/groupadd -o -r weston-launch

%docs_package

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/wcap-*
%{_bindir}/weston
%{_bindir}/weston-info
%attr(4755,root,root) %{_bindir}/weston-launch
%{_bindir}/weston-terminal
%{_libexecdir}/weston-*
%{_libdir}/weston/desktop-shell.so
%{_libdir}/weston/drm-backend.so
%{_libdir}/weston/fbdev-backend.so
%{_libdir}/weston/fullscreen-shell.so
%{_libdir}/weston/headless-backend.so
%{_libdir}/weston/wayland-backend.so
%{_libdir}/weston/gl-renderer.so
%{_libdir}/weston/ivi-shell.so
%{_libdir}/weston/ivi-layout.so
%{_libdir}/weston/hmi-controller.so
%{_datadir}/weston
%{_unitdir_user}/weston.target

%files devel
%manifest %{name}.manifest
%{_includedir}/weston/*.h
%{_libdir}/pkgconfig/*.pc

%files clients
%manifest %{name}.manifest
%{_bindir}/weston-simple-touch
%{_bindir}/weston-simple-shm
%{_bindir}/weston-simple-egl
%{_bindir}/weston-flower
%{_bindir}/weston-image
%{_bindir}/weston-cliptest
%{_bindir}/weston-dnd
%{_bindir}/weston-editor
%{_bindir}/weston-smoke
%{_bindir}/weston-resizor
%{_bindir}/weston-eventdemo
%{_bindir}/weston-clickdot
%{_bindir}/weston-subsurfaces
%{_bindir}/weston-transformed
%{_bindir}/weston-fullscreen
%{_bindir}/weston-calibrator

%if %{with rdp}
%files rdp
%manifest %{name}.manifest
%{_libdir}/weston/rdp-backend.so
%endif

%changelog
