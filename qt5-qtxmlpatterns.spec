#
# Conditional build:
%bcond_without	doc	# Documentation
%bcond_without	qm	# QM translations
%bcond_without	qml	# Quick xmllistmodel plugin

%define		orgname			qtxmlpatterns
%define		qtbase_ver		%{version}
%define		qttools_ver		5.9
%define		qtdeclarative_ver	%{version}
Summary:	The Qt5 XmlPatterns library
Summary(pl.UTF-8):	Biblioteka Qt5 XmlPatterns
Name:		qt5-%{orgname}
Version:	5.15.17
Release:	1
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	739688b040c32efd557c0834adbc44c5
Source1:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/qttranslations-everywhere-opensource-src-%{version}.tar.xz
# Source1-md5:	e20cfdef4f3088ca568f7e43ab5bba8c
URL:		https://www.qt.io/
BuildRequires:	OpenGL-devel
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
%{?with_qml:BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
%{?with_qm:BuildRequires:	qt5-linguist >= %{qttools_ver}}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
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
%requires_eq_to	Qt5Core Qt5Core-devel
Requires:	Qt5Network >= %{qtbase_ver}
Obsoletes:	qt5-qtxmlpatterns < 5.3.0

%description -n Qt5XmlPatterns
Qt5 XmlPatterns library provides support for XPath, XQuery, XSLT and
XML Schema validation.

%description -n Qt5XmlPatterns -l pl.UTF-8
Biblioteka Qt5 XmlPatterns zapewnia obsługę XPath, XQuery, XSLT oraz
sprawdzanie poprawności wg XML Schema.

%package -n Qt5XmlPatterns-devel
Summary:	Qt5 XmlPatterns library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 XmlPatterns - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Network-devel >= %{qtbase_ver}
Requires:	Qt5XmlPatterns = %{version}-%{release}
Obsoletes:	qt5-qtxmlpatterns-devel < 5.3.0

%description -n Qt5XmlPatterns-devel
Qt5 XmlPatterns library - development files.

%description -n Qt5XmlPatterns-devel -l pl.UTF-8
Biblioteka Qt5 XmlPatterns - pliki programistyczne.

%package -n Qt5Quick-xmllistmodel
Summary:	XmlListModel plugin for Qt5 Quick
Summary(pl.UTF-8):	Wtyczka XmlListModel dla Qt5 Quick
Group:		X11/Libraries
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Requires:	Qt5Quick >= %{qtdeclarative_ver}
Requires:	Qt5XmlPatterns = %{version}-%{release}

%description -n Qt5Quick-xmllistmodel
XmlListModel plugin for Qt5 Quick provides QML types for creating
models from XML data.

%description -n Qt5Quick-xmllistmodel -l pl.UTF-8
Wtyczka XmlListModel dla Qt5 Quick dostarcza typy QML do tworzenia
modeli z danych XML.

%package doc
Summary:	Qt5 XmlPatterns documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 XmlPatterns w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 XmlPatterns documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 XmlPatterns w formacie HTML.

%package doc-qch
Summary:	Qt5 XmlPatterns documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 XmlPatterns w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 XmlPatterns documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 XmlPatterns w formacie QCH.

%package examples
Summary:	Qt5 XmlPatterns examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 XmlPatterns
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Qt5 XmlPatterns examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 XmlPatterns.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version} %{?with_qm:-a1}

%build
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%if %{with qm}
cd qttranslations-everywhere-src-%{version}
%{qmake_qt5}
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

%if %{with qm}
%{__make} -C qttranslations-everywhere-src-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
# keep only qtxmlpatterns
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qt5/translations/{assistant,designer,linguist,qt,qtbase,qtconnectivity,qtdeclarative,qtlocation,qtmultimedia,qtquickcontrols,qtquickcontrols2,qtserialport,qtscript,qtwebengine,qtwebsockets}_*.qm
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
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

# find_lang --with-qm supports only PLD qt3/qt4 specific %{_datadir}/locale/*/LC_MESSAGES layout
find_qt5_qm()
{
	name="$1"
	find $RPM_BUILD_ROOT%{_datadir}/qt5/translations -name "${name}_*.qm" | \
		sed -e "s:^$RPM_BUILD_ROOT::" \
		    -e 's:\(.*/'$name'_\)\([a-z][a-z][a-z]\?\)\(_[A-Z][A-Z]\)\?\(\.qm\)$:%lang(\2\3) \1\2\3\4:'
}

echo '%defattr(644,root,root,755)' > qtxmlpatterns.lang
%if %{with qm}
find_qt5_qm qtxmlpatterns >> qtxmlpatterns.lang
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5XmlPatterns -p /sbin/ldconfig
%postun	-n Qt5XmlPatterns -p /sbin/ldconfig

%files -n Qt5XmlPatterns -f qtxmlpatterns.lang
%defattr(644,root,root,755)
%doc LICENSE.GPL3-EXCEPT dist/changes-*
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

%if %{with qml}
%files -n Qt5Quick-xmllistmodel
%defattr(644,root,root,755)
%dir %{qt5dir}/qml/QtQuick/XmlListModel
%{qt5dir}/qml/QtQuick/XmlListModel/libqmlxmllistmodelplugin.so
%{qt5dir}/qml/QtQuick/XmlListModel/plugins.qmltypes
%{qt5dir}/qml/QtQuick/XmlListModel/qmldir
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtxmlpatterns

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtxmlpatterns.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
