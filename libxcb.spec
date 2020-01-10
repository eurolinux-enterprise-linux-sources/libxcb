%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:       libxcb
Version:    1.11
Release:    4%{?dist}
Summary:    A C binding to the X11 protocol
License:    MIT
URL:        http://xcb.freedesktop.org/

Source0:    http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
Patch1:     libxcb-expose-64-bit-sequence-numbers-for-XLib.patch

# This is stolen straight from the pthread-stubs source:
# http://cgit.freedesktop.org/xcb/pthread-stubs/blob/?id=6900598192bacf5fd9a34619b11328f746a5956d
# we don't need the library because glibc has working pthreads, but we need
# the pkgconfig file so libs that link against libxcb know this...
Source1:    pthread-stubs.pc.in

BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libtool
BuildRequires:  libxslt
BuildRequires:  pkgconfig(xau) >= 0.99.2
BuildRequires:  pkgconfig(xcb-proto) >= 1.11
BuildRequires:  pkgconfig(xorg-macros) >= 1.18
#BuildRequires:  xorg-x11-proto-devel

%description
The X protocol C-language Binding (XCB) is a replacement for Xlib featuring a
small footprint, latency hiding, direct access to the protocol, improved
threading support, and extensibility.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%package doc
Summary:    Documentation for %{name}
BuildArch:  noarch

%description doc
The %{name}-doc package contains documentation for the %{name} library.

%prep
%setup -q 
%patch1 -p1 -b .64bit-seqno

%build
sed -i 's/pthread-stubs //' configure.ac
autoreconf -v --install
%configure \
    --disable-static \
    --docdir=%{_pkgdocdir} \
    --enable-selinux \
    --enable-xkb \
    --enable-xinput \
    --disable-xprint
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
install -pm 644 COPYING NEWS README $RPM_BUILD_ROOT%{_pkgdocdir}
sed 's,@libdir@,%{_libdir},;s,@prefix@,%{_prefix},;s,@exec_prefix@,%{_exec_prefix},' %{SOURCE1} \
    > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/pthread-stubs.pc

find $RPM_BUILD_ROOT -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libxcb-composite.so.0*
%{_libdir}/libxcb-damage.so.0*
%{_libdir}/libxcb-dpms.so.0*
%{_libdir}/libxcb-dri2.so.0*
%{_libdir}/libxcb-dri3.so.0*
%{_libdir}/libxcb-glx.so.0*
%{_libdir}/libxcb-present.so.0*
%{_libdir}/libxcb-randr.so.0*
%{_libdir}/libxcb-record.so.0*
%{_libdir}/libxcb-render.so.0*
%{_libdir}/libxcb-res.so.0*
%{_libdir}/libxcb-screensaver.so.0*
%{_libdir}/libxcb-shape.so.0*
%{_libdir}/libxcb-shm.so.0*
%{_libdir}/libxcb-sync.so.1*
%{_libdir}/libxcb-xevie.so.0*
%{_libdir}/libxcb-xf86dri.so.0*
%{_libdir}/libxcb-xfixes.so.0*
%{_libdir}/libxcb-xinerama.so.0*
%{_libdir}/libxcb-xinput.so.0*
%{_libdir}/libxcb-xkb.so.1*
%{_libdir}/libxcb-xselinux.so.0*
%{_libdir}/libxcb-xtest.so.0*
%{_libdir}/libxcb-xv.so.0*
%{_libdir}/libxcb-xvmc.so.0*
%{_libdir}/libxcb.so.1*

%files devel
%{_includedir}/xcb
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*

%files doc
%{_pkgdocdir}

%changelog
* Mon Jun 08 2015 Olivier Fourdan <ofourdan@redhat.com> 1.11-4
- Add 64bit sequence number API for Xlib (#1206245)

* Thu Jan 08 2015 Simone Caronni <negativo17@gmail.com> - 1.11-3
- Clean up SPEC file, fix rpmlint warnings.
- Enable XInput extension (#1177701).

* Fri Oct 24 2014 Dan Horák <dan@danny.cz> - 1.11-2
- rebuilt for broken koji db - no buildroot info

* Wed Oct 01 2014 Adam Jackson <ajax@redhat.com> 1.11-1
- libxcb 1.11

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 27 2014 Adam Jackson <ajax@redhat.com> 1.10-1
- libxcb 1.10 plus one. Updated ABIs: sync, xkb. New libs: dri3, present.

* Tue Aug  6 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.9.1-3
- Install docs to %%{_pkgdocdir} where available.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-1
- libxcb 1.9.1

* Fri May 24 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.9-3
- Fix integer overflow in read_packet (CVE-2013-2064)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Adam Jackson <ajax@redhat.com> 1.9-1
- libxcb 1.9

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 1.8.1-4
- --enable-xkb for weston
- --disable-xprint instead of manual rm
- BuildRequire an updated xcb-proto for XKB and DRI2 fixes

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 09 2012 Adam Jackson <ajax@redhat.com> 1.8.1-1
- libxcb 1.8.1

* Fri Jan 13 2012 Adam Jackson <ajax@redhat.com> 1.8-2
- Don't %%doc in the base package, that pulls in copies of things we only
  want in -doc subpackage.

* Wed Jan 11 2012 Adam Jackson <ajax@redhat.com> 1.8-1
- libxcb 1.8
