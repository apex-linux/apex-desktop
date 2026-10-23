# SPDX-License-Identifier: GPL-3.0-or-later
#
# No scriptlets: the image and glib2's file trigger compile the schemas, the image runs
# dconf update; no unit has [Install].

%{!?commitdate:%global commitdate 0}
%{!?shortcommit:%global shortcommit unknown}
# Colloid's app icons; make rpm fetches this commit and archives the Makefile's COLLOID_PATHS.
%global colloid_commit ceac6608ecd0e40025cbc2ebbd32bf0e0f4ebc6a
%global colloid_sha256 e81d7d9d3a473c0772f9a3afe762d6ec5b7f2292655466e9a1ac32590ba093f0

Name:           apex-desktop
Version:        0.1.0
Release:        0.%{commitdate}.git%{shortcommit}%{?dist}
Summary:        Apex desktop data: the Apex GSettings schema, vendor defaults, the shell crash guard, the wallpapers and the Apex icon theme

# Colloid's app icons ship the GPLv3 text and state no version beyond it.
License:        GPL-3.0-or-later AND GPL-3.0-only
URL:            https://github.com/apex-linux/apex-desktop
Source0:        %{name}-%{version}.tar.gz
Source1:        Colloid-icon-theme-%{colloid_commit}.tar

BuildArch:      noarch

BuildRequires:  /usr/bin/glib-compile-schemas
BuildRequires:  /usr/bin/inkscape
BuildRequires:  /usr/bin/rsvg-convert
BuildRequires:  /usr/bin/xmllint
BuildRequires:  systemd-rpm-macros

# apex-shell-safe.service runs gsettings.
Requires:       /usr/bin/gsettings
# The Apex theme inherits both, and icon-theme='Apex' relies on it.
Requires:       adwaita-icon-theme
Requires:       hicolor-icon-theme
Requires:       dconf
Requires:       fontconfig
Requires:       gnome-control-center-filesystem

%description
Data files of the Apex desktop. This build ships the io.github.apex_linux.Apex.Desktop
GSettings schema, with its Keybindings child: the settings of the Apex layer in the
rebuilt gnome-shell. The layer treats a missing schema as safe mode. It ships Apex's
vendor defaults for GNOME's own schemas, the Open Spotlight row of Settings > Keyboard,
the ss03 feature of Adwaita Sans, and the default Ptyxis profile. It also ships the
crash guard: when GNOME Shell fails within 60 seconds of the layer's enable,
apex-shell-safe.service sets layer-enabled to false for that user. The light and dark
Apex Facets wallpapers ship as PNGs, paired for GNOME's background chooser. The Apex
icon theme carries Colloid's full-colour app icons and the Apex Symbolic glyphs, with
their strokes turned into fills, and inherits Adwaita and hicolor.

%prep
%autosetup -n %{name}-%{version}
echo '%{colloid_sha256}  %{SOURCE1}' | sha256sum -c -
tar -xf %{SOURCE1}
cp -p Colloid-icon-theme-%{colloid_commit}/LICENSE LICENSE.Colloid

%build
# 3840x2400 covers the laptop's 2880x1800 panel and a 4K monitor.
rsvg-convert -w 3840 -h 2400 -o apex-facets-light.png desktop/wallpapers/apex-facets-light.svg
rsvg-convert -w 3840 -h 2400 -o apex-facets-dark.png desktop/wallpapers/apex-facets-dark.svg
mkdir symbolic
# Ungrouping moves a group's stroke onto its children, so stroke-to-path reaches every stroke.
for f in desktop/icons/symbolic/*.svg; do
    n=${f##*/}
    inkscape --actions="select-all:all;selection-ungroup;select-all:all;selection-ungroup;select-all:all;object-stroke-to-path;export-plain-svg;export-filename:$PWD/symbolic/${n%.svg}-symbolic.svg;export-do" "$f"
done

%install
install -Dm0644 desktop/schemas/io.github.apex_linux.Apex.Desktop.gschema.xml \
    %{buildroot}%{_datadir}/glib-2.0/schemas/io.github.apex_linux.Apex.Desktop.gschema.xml
install -Dm0644 desktop/systemd/user/apex-shell-safe.service \
    %{buildroot}%{_userunitdir}/apex-shell-safe.service
install -Dm0644 'desktop/systemd/user/org.gnome.Shell@.service.d/50-apex.conf' \
    '%{buildroot}%{_userunitdir}/org.gnome.Shell@.service.d/50-apex.conf'
install -Dm0644 desktop/schemas/90_apex.gschema.override \
    %{buildroot}%{_datadir}/glib-2.0/schemas/90_apex.gschema.override
install -Dm0644 desktop/dconf/distro.d/50-apex-ptyxis \
    %{buildroot}%{_sysconfdir}/dconf/db/distro.d/50-apex-ptyxis
install -Dm0644 desktop/keybindings/60-apex.xml \
    %{buildroot}%{_datadir}/gnome-control-center/keybindings/60-apex.xml
install -Dm0644 desktop/fontconfig/60-apex-adwaita-sans-ss03.conf \
    %{buildroot}%{_datadir}/fontconfig/conf.avail/60-apex-adwaita-sans-ss03.conf
install -dm0755 %{buildroot}%{_sysconfdir}/fonts/conf.d
ln -s ../../..%{_datadir}/fontconfig/conf.avail/60-apex-adwaita-sans-ss03.conf \
    %{buildroot}%{_sysconfdir}/fonts/conf.d/60-apex-adwaita-sans-ss03.conf
install -Dm0644 apex-facets-light.png %{buildroot}%{_datadir}/backgrounds/apex/apex-facets-light.png
install -Dm0644 apex-facets-dark.png %{buildroot}%{_datadir}/backgrounds/apex/apex-facets-dark.png
install -Dm0644 desktop/wallpapers/apex-facets.xml \
    %{buildroot}%{_datadir}/gnome-background-properties/apex-facets.xml
install -Dm0644 desktop/icons/index.theme %{buildroot}%{_datadir}/icons/Apex/index.theme
install -Dm0644 -t %{buildroot}%{_datadir}/icons/Apex/symbolic symbolic/*-symbolic.svg
install -dm0755 %{buildroot}%{_datadir}/icons/Apex/scalable/apps
cp -a Colloid-icon-theme-%{colloid_commit}/src/apps/scalable/. \
    Colloid-icon-theme-%{colloid_commit}/links/apps/scalable/. \
    %{buildroot}%{_datadir}/icons/Apex/scalable/apps/
# Colloid links a few names to icons it does not ship, and one symbolic name to a colour icon.
find %{buildroot}%{_datadir}/icons/Apex/scalable/apps \( -xtype l -o -name '*-symbolic.svg' \) -print -delete

%check
glib-compile-schemas --strict --dry-run %{buildroot}%{_datadir}/glib-2.0/schemas
bash desktop/icons/check-theme.sh %{buildroot}%{_datadir}/icons/Apex

%files
%license LICENSE
%license LICENSE.Colloid
%{_datadir}/glib-2.0/schemas/io.github.apex_linux.Apex.Desktop.gschema.xml
%{_datadir}/glib-2.0/schemas/90_apex.gschema.override
%{_datadir}/gnome-control-center/keybindings/60-apex.xml
%{_datadir}/fontconfig/conf.avail/60-apex-adwaita-sans-ss03.conf
%config(noreplace) %{_sysconfdir}/fonts/conf.d/60-apex-adwaita-sans-ss03.conf
%config(noreplace) %{_sysconfdir}/dconf/db/distro.d/50-apex-ptyxis
%{_userunitdir}/apex-shell-safe.service
# gnome-shell ships no drop-in directory for its unit, so this package owns it.
%dir %{_userunitdir}/org.gnome.Shell@.service.d
%{_userunitdir}/org.gnome.Shell@.service.d/50-apex.conf
%dir %{_datadir}/backgrounds/apex
%{_datadir}/backgrounds/apex/apex-facets-light.png
%{_datadir}/backgrounds/apex/apex-facets-dark.png
%dir %{_datadir}/gnome-background-properties
%{_datadir}/gnome-background-properties/apex-facets.xml
%{_datadir}/icons/Apex/

%changelog
* Fri Oct 23 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- The Apex icon theme: Colloid's app icons from a pinned commit, Apex Symbolic glyphs
  turned into fills with Inkscape, Inherits=Adwaita,hicolor
- icon-theme='Apex' in the vendor override

* Fri Oct 23 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- The Apex Ptyxis profile: the default, with line height 1.21, in dconf's distro database

* Fri Oct 23 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- The rest of the Apex schema and its Keybindings child (toggle-spotlight)
- 90_apex.gschema.override moves here from the image, with the S1b vendor defaults
- 60-apex.xml: Open Spotlight in Settings > Keyboard
- The wallpapers as 3840x2400 PNGs, with a gnome-background-properties entry
- fontconfig: ss03 for Adwaita Sans

* Fri Oct 23 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- The Apex Facets wallpapers, light and dark, in /usr/share/backgrounds/apex

* Mon Sep 28 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- The shell crash guard: apex-shell-safe.service and the drop-in on org.gnome.Shell@.service
- First package: the Apex GSettings schema, layer-enabled and disabled-features (S1a)
