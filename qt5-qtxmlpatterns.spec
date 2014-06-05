# TODO:
# - cleanup
#
# Conditional build:
%bcond_without	qch	# documentation in QCH format

%define		orgname		qtxmlpatterns
%define		qtbase_ver	%{version}
%define		qttools_ver	%{version}
Summary:	The Qt5 XmlPatterns
Name:		qt5-%{orgname}
Version:	5.2.0
Release:	0.1
License:	LGPL v2.1 or GPL v3.0
Group:		X11/Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	7c3e94cd04603c3f81e50d47daf5bbc7
URL:		http://qt-project.org/
BuildRequires:	qt5-qtbase-devel >= %{qtbase_ver}
%if %{with qch}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 XmlPatterns libraries.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera biblioteki Qt5 XmlPatterns.

%package -n Qt5XmlPatterns
Summary:	The Qt5 XmlPatterns library
Summary(pl.UTF-8):	Biblioteka Qt5 XmlPatterns
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Obsoletes:	qt5-qtxmlpatterns

%description -n Qt5XmlPatterns
Qt5 XmlPatterns library.

%description -n Qt5XmlPatterns -l pl.UTF_8
Biblioteka Qt5 XmlPatterns.

%package -n Qt5XmlPatterns-devel
Summary:	Qt5 XmlPatterns library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 XmlPatterns - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5XmlPatterns = %{version}-%{release}
Obsoletes:	qt5-qtxmlpatterns-devel

%description -n Qt5XmlPatterns-devel
Qt5 XmlPatterns library - development files.

%description -n Qt5XmlPatterns-devel -l pl.UTF-8
Biblioteka Qt5 XmlPatterns - pliki programistyczne.

%package doc
Summary:	Qt5 XmlPatterns documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 XmlPatterns w formacie HTML
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 XmlPatterns documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 XmlPatterns w formacie HTML.

%package doc-qch
Summary:	Qt5 XmlPatterns documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 XmlPatterns w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 XmlPatterns documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 XmlPatterns w formacie QCH.

%package examples
Summary:	Qt5 XmlPatterns examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 XmlPatterns
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Qt5 XmlPatterns examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 XmlPatterns.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5
%{__make}
%{__make} %{!?with_qch:html_}docs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_%{!?with_qch:html_}docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.?
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	RESULT=`echo $RPM_BUILD_ROOT$2 2>/dev/null`
	[ "$RESULT" == "" ] && return # XXX this is never true due $RPM_BUILD_ROOT being set
	r=`echo $RESULT | awk '{ print $1 }'`

	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho examples %{_examplesdir}/qt5
for f in `find $RPM_BUILD_ROOT%{_examplesdir}/qt5 -printf "%%P "`; do
	ifecho examples %{_examplesdir}/qt5/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5XmlPatterns -p /sbin/ldconfig
%postun	-n Qt5XmlPatterns -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5XmlPatterns.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5XmlPatterns.so.5
%attr(755,root,root) %{qt5dir}/bin/xmlpatterns*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5XmlPatterns.so
%{_libdir}/libQt5XmlPatterns.prl
%{_includedir}/qt5/QtXmlPatterns
%{_pkgconfigdir}/Qt5XmlPatterns.pc
%{_libdir}/cmake/Qt5XmlPatterns
%{qt5dir}/mkspecs/modules/*.pri

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtxmlpatterns

%if %{with qch}
%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtxmlpatterns.qch
%endif

%files examples -f examples.files
