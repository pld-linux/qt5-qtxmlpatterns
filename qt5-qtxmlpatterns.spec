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
Version:	5.3.0
Release:	1
License:	LGPL v2.1 or GPL v3.0
Group:		X11/Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.3/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	68c6e1311ecf8727368961739243d3b2
URL:		http://qt-project.org/
BuildRequires:	OpenGL-devel
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
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
Requires:	Qt5Network >= %{qtbase_ver}
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
Requires:	Qt5Network-devel >= %{qtbase_ver}
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

# symlinks in system bin dir
install -d $RPM_BUILD_ROOT%{_bindir}
cd $RPM_BUILD_ROOT%{_bindir}
ln -sf ../%{_lib}/qt5/bin/xmlpatterns xmlpatterns-qt5
ln -sf ../%{_lib}/qt5/bin/xmlpatternsvalidator xmlpatternsvalidator-qt5
cd -

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
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
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/xmlpatterns

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5XmlPatterns -p /sbin/ldconfig
%postun	-n Qt5XmlPatterns -p /sbin/ldconfig

%files -n Qt5XmlPatterns
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt dist/changes-*
%attr(755,root,root) %{_libdir}/libQt5XmlPatterns.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5XmlPatterns.so.5
%attr(755,root,root) %{_bindir}/xmlpatterns-qt5
%attr(755,root,root) %{_bindir}/xmlpatternsvalidator-qt5
%attr(755,root,root) %{qt5dir}/bin/xmlpatterns
%attr(755,root,root) %{qt5dir}/bin/xmlpatternsvalidator

%files -n Qt5XmlPatterns-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5XmlPatterns.so
%{_libdir}/libQt5XmlPatterns.prl
%{_includedir}/qt5/QtXmlPatterns
%{_pkgconfigdir}/Qt5XmlPatterns.pc
%{_libdir}/cmake/Qt5XmlPatterns
%{qt5dir}/mkspecs/modules/qt_lib_xmlpatterns.pri
%{qt5dir}/mkspecs/modules/qt_lib_xmlpatterns_private.pri

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtxmlpatterns

%if %{with qch}
%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtxmlpatterns.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
