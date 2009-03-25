# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#%define buildforkernels newest

Name:           blcr-kmod
Version:        0.8.0
Release:        2%{?dist}.4
Summary:        Kernel module (kmod) for Berkeley Lab Checkpoint/Restart for Linux

%define distname blcr-%{version}

Group:          System Environment/Base
License:        GPLv2+
URL:            http://www.blcr.org/
Source0:        http://ftg.lbl.gov/CheckpointRestart/downloads/%{distname}.tar.gz
# Patch0 is to remove -fno-stack-protector (provided by upstream)
# Patch0 requires running autoreconf
#Patch0:		blcr-stackcheck.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#Generic i386 is NOT supported
# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64 ppc ppc64

# get the needed BuildRequires (in parts depending on what we build for)
#BuildRequires:  %{_bindir}/kmodtool autoconf automake libtool
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Kernel modules for Berkeley Lab Checkpoint/Restart for Linux (BLCR)
These kernel modules are built for Linux %{kernel}.

You must also install the base %{name} package.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0 -n %{distname}
# apply patches and do other stuff here
#pushd %{real_distname}
#%patch0 -p0
#patch0 modified configure.ac, Makefile.am
#autoreconf --force --install
#popd

for kernel_version  in %{?kernel_versions} ; do
    cp -a %{distname} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
    pushd _kmod_build_${kernel_version%%___*}
        %configure --with-kmod-dir=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} --with-installed-libcr --with-installed-util --with-linux="${kernel_version##*___}" 
        make modules
    popd
done


%install
rm -rf $RPM_BUILD_ROOT
for kernel_version  in %{?kernel_versions} ; do
        make -C _kmod_build_${kernel_version%%___*} DESTDIR=$RPM_BUILD_ROOT KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} install
#       mkdir -p $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
#       mv $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/../*.ko $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
        chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/*
done

%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Mar 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.8.0-2.4
- rebuild for new kernels

* Wed Mar 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.8.0-2.3
- rebuild for new kernels

* Tue Feb 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.8.0-2.2
- rebuild for latest Fedora kernel;

* Fri Feb 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.8.0-2.1
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Neal Becker <ndbecker2@gmail.com> - 0.8.0-2
- Put back EA i686
- Copy 1st 6 lines from http://cvs.rpmfusion.org/viewvc/rpms/madwifi-kmod/devel/madwifi-kmod.spec?root=nonfree&view=markup

* Fri Jan 16 2009 Neal Becker <ndbecker2@gmail.com> - 0.8.0-1
- Update to 0.8.0 release

* Mon Dec 22 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0-0.1.b5
- BR automake
- BR libtool
- Change version release to match package guidelines

* Mon Dec 22 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0_b5-4
- Make release match blcr

* Mon Dec 22 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0_b5-2
- Try patch to remove -fno-stack-protector
- Force autoreconf (for patch0)

* Thu Dec 18 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0_b5-1
- Update to 0.8.0_b5

* Mon Dec  1 2008 Neal Becker <ndbecker2@gmail.com> - 0.8.0_b1-1
- Update to 0.8.0b1

* Sun Nov 30 2008 Neal Becker <ndbecker2@gmail.com> - 0.7.3-1
- Update to 0.7.3

* Fri Jun 13 2008 Neal Becker <ndbecker2@gmail.com> - 0.7.0-1
- Update to 0.7.0

* Sat Mar  1 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.5-1
- Update to 0.6.5

* Sun Feb  3 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.4-3
- Remove filterfile
- Misc cleanups

* Tue Jan 29 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.4-1
- Update to 0.6.4
- Try --with-kmod-dir

* Mon Jan 28 2008 Neal Becker <ndbecker2@gmail.com> - 0.6.3-1
- Initial akmods version

