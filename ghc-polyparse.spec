#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	polyparse
Summary:	A variety of alternative parser combinator libraries
Name:		ghc-%{pkgname}
Version:	1.12
Release:	1
License:	LGPL
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/polyparse
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	d925e7a465a65c1b41b8acc40cc19d39
URL:		http://hackage.haskell.org/package/polyparse
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base < 6
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-text
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof < 6
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-text-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base < 6
Requires:	ghc-bytestring
Requires:	ghc-text
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
A variety of alternative parser combinator libraries, including the
original HuttonMeijer set. The Poly sets have features like good error
reporting, arbitrary token type, running state, lazy parsing, and so
on. Finally, Text.Parse is a proposed replacement for the standard
Read class, for better deserialisation of Haskell values from Strings.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof < 6
Requires:	ghc-bytestring-prof
Requires:	ghc-text-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSpolyparse-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSpolyparse-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parse
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parse/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/Poly
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/Poly/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSpolyparse-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Parse/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/ParserCombinators/Poly/*.p_hi
%endif
