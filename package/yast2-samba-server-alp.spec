#
# spec file for package yast2-samba-server-alp
#
# Copyright (c) 2023 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           yast2-samba-server-alp
Version:        0.1
Release:        0
Summary:        YaST2 - Samba Containerized Server Configuration
License:        GPL-3.0-only
Group:          Productivity/Networking/Samba
Url:            https://github.com/yast/yast2-samba-server-alp

Source:         %{name}-%{version}.tar.bz2

BuildRequires:  perl-XML-Writer
BuildRequires:  python3
BuildRequires:  update-desktop-files
BuildRequires:  yast2
BuildRequires:  yast2-devtools
BuildRequires:  yast2-testsuite
BuildRequires:  rubygem(%rb_default_ruby_abi:yast-rake)

Requires:       yast2
Requires:       yast2-python3-bindings >= 4.0.0

BuildArch:      noarch

%description
This package contains the YaST2 component for configuring
a Samba server in a container.

%prep
%setup -q

%build

%install
%yast_install

%files
%{yast_clientdir}
%{yast_yncludedir}
%{yast_desktopdir}
%doc %{yast_docdir}
%license COPYING

%changelog
