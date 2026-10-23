# SPDX-License-Identifier: GPL-3.0-or-later
#
# No scriptlets: the image and glib2's file trigger compile the schemas; no unit has [Install].

%{!?commitdate:%global commitdate 0}
%{!?shortcommit:%global shortcommit unknown}

Name:           apex-desktop
Version:        0.1.0
Release:        0.%{commitdate}.git%{shortcommit}%{?dist}
Summary:        Apex desktop data: the Apex GSettings schema, the shell crash guard and the wallpapers

License:        GPL-3.0-or-later
URL:            https://github.com/SekiroKenjii/apex-fedora
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  /usr/bin/glib-compile-schemas
BuildRequires:  systemd-rpm-macros

# apex-shell-safe.service runs gsettings.
Requires:       /usr/bin/gsettings

%description
Data files of the Apex desktop. This build ships the io.github.sekirokenjii.Apex.Desktop
GSettings schema: layer-enabled and disabled-features, the switches of the Apex layer
in the rebuilt gnome-shell. The layer treats a missing schema as safe mode. It also
ships the crash guard: when GNOME Shell fails within 60 seconds of the layer's enable,
apex-shell-safe.service sets layer-enabled to false for that user. The light and dark
Apex Facets wallpapers ship too.

%prep
%autosetup -n %{name}-%{version}

%build

%install
install -Dm0644 desktop/schemas/io.github.sekirokenjii.Apex.Desktop.gschema.xml \
    %{buildroot}%{_datadir}/glib-2.0/schemas/io.github.sekirokenjii.Apex.Desktop.gschema.xml
install -Dm0644 desktop/systemd/user/apex-shell-safe.service \
    %{buildroot}%{_userunitdir}/apex-shell-safe.service
install -Dm0644 'desktop/systemd/user/org.gnome.Shell@.service.d/50-apex.conf' \
    '%{buildroot}%{_userunitdir}/org.gnome.Shell@.service.d/50-apex.conf'
install -Dm0644 desktop/wallpapers/apex-facets-light.svg \
    %{buildroot}%{_datadir}/backgrounds/apex/apex-facets-light.svg
install -Dm0644 desktop/wallpapers/apex-facets-dark.svg \
    %{buildroot}%{_datadir}/backgrounds/apex/apex-facets-dark.svg

%check
glib-compile-schemas --strict --dry-run %{buildroot}%{_datadir}/glib-2.0/schemas

%files
%license LICENSE
%{_datadir}/glib-2.0/schemas/io.github.sekirokenjii.Apex.Desktop.gschema.xml
%{_userunitdir}/apex-shell-safe.service
# gnome-shell ships no drop-in directory for its unit, so this package owns it.
%dir %{_userunitdir}/org.gnome.Shell@.service.d
%{_userunitdir}/org.gnome.Shell@.service.d/50-apex.conf
%dir %{_datadir}/backgrounds/apex
%{_datadir}/backgrounds/apex/apex-facets-light.svg
%{_datadir}/backgrounds/apex/apex-facets-dark.svg

%changelog
* Fri Oct 23 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- The Apex Facets wallpapers, light and dark, in /usr/share/backgrounds/apex

* Mon Sep 28 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- The shell crash guard: apex-shell-safe.service and the drop-in on org.gnome.Shell@.service
- First package: the Apex GSettings schema, layer-enabled and disabled-features (S1a)
