# SPDX-License-Identifier: GPL-3.0-or-later
#
# apex-desktop: the data files of the Apex desktop (ARCHITECTURE 7.4; ADR 0014), built
# from desktop/ except desktop/shell/, which ships inside the rebuilt gnome-shell. In S1a
# it holds only the Apex GSettings schema, whose two keys are the layer's safety net
# (layer-enabled, disabled-features). S1b adds the icon theme, the Plymouth themes, the
# wallpaper, fontconfig, the Ptyxis defaults and the vendor override. It is separate from
# the Rust apex RPM, so an asset change never rebuilds cargo.
#
# Build it with `make rpm-desktop` from a git checkout (packaging/README.md). That runs
# `git archive HEAD` of desktop/ (without desktop/shell/) and LICENSE into Source0, and
# rpmbuild with the commitdate and shortcommit macros of `make rpm`.
#
# No scriptlets: the image compiles the schemas in its final stage, and glib2's file
# trigger covers a dnf install.

# Local builds without the macros still work; they get the lowest possible Release.
%{!?commitdate:%global commitdate 0}
%{!?shortcommit:%global shortcommit unknown}

Name:           apex-desktop
Version:        0.1.0
Release:        0.%{commitdate}.git%{shortcommit}%{?dist}
Summary:        Apex desktop data: the Apex GSettings schema

# Apex's own files. From S1b also Colloid's icons (GPL-3.0) and, from S5, glyphs derived
# from Hugeicons (MIT).
License:        GPL-3.0-or-later
URL:            https://github.com/SekiroKenjii/apex-fedora
# Produced by `make rpm-desktop`: git archive --prefix=apex-desktop-%%{version}/ HEAD
# desktop ':(exclude)desktop/shell' LICENSE
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  /usr/bin/glib-compile-schemas

%description
Data files of the Apex desktop. This build ships the io.github.sekirokenjii.Apex.Desktop
GSettings schema: layer-enabled and disabled-features, the switches of the Apex layer
in the rebuilt gnome-shell. The layer treats a missing schema as safe mode.

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to build.

%install
install -Dm0644 desktop/schemas/io.github.sekirokenjii.Apex.Desktop.gschema.xml \
    %{buildroot}%{_datadir}/glib-2.0/schemas/io.github.sekirokenjii.Apex.Desktop.gschema.xml

%check
# --strict fails on an unknown type, a bad default or a duplicate key.
glib-compile-schemas --strict --dry-run %{buildroot}%{_datadir}/glib-2.0/schemas

%files
%license LICENSE
%{_datadir}/glib-2.0/schemas/io.github.sekirokenjii.Apex.Desktop.gschema.xml

%changelog
* Mon Sep 28 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- First package: the Apex GSettings schema, layer-enabled and disabled-features (S1a)
