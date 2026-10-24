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
Summary:        Apex desktop data: the Apex GSettings schema, vendor defaults, the shell crash guard, the wallpapers, the Apex icon theme and the boot splash

# Colloid's app icons ship the GPLv3 text and state no version beyond it.
License:        GPL-3.0-or-later AND GPL-3.0-only
URL:            https://github.com/apex-linux/apex-desktop
Source0:        %{name}-%{version}.tar.gz
Source1:        Colloid-icon-theme-%{colloid_commit}.tar

BuildArch:      noarch

BuildRequires:  /usr/bin/fc-match
BuildRequires:  /usr/bin/glib-compile-schemas
BuildRequires:  /usr/bin/gtk-update-icon-cache
BuildRequires:  /usr/bin/inkscape
BuildRequires:  /usr/bin/rsvg-convert
BuildRequires:  /usr/bin/xmllint
BuildRequires:  adwaita-sans-fonts
BuildRequires:  systemd-rpm-macros

# apex-shell-safe.service runs gsettings.
Requires:       /usr/bin/gsettings
# apex-folder-icons sets folder metadata with gio, in the shell's translation of Screenshots.
Requires:       /usr/bin/gio
Requires:       /usr/bin/gettext
Requires:       /usr/bin/xdg-user-dir
# The Apex theme inherits both, and icon-theme='Apex' relies on it.
Requires:       adwaita-icon-theme
Requires:       hicolor-icon-theme
Requires:       dconf
Requires:       fontconfig
Requires:       gnome-control-center-filesystem
Requires:       plymouth-plugin-script
Requires:       plymouth-plugin-two-step

%description
Data files of the Apex desktop. This build ships the io.github.apex_linux.Apex.Desktop
GSettings schema, with its Keybindings child: the settings of the Apex layer in the
rebuilt gnome-shell. The layer treats a missing schema as safe mode. It ships Apex's
vendor defaults for GNOME's own schemas, the Open Spotlight row of Settings > Keyboard,
the ss03 feature of Adwaita Sans, the default Ptyxis profile and the coloured bash
prompt. It also ships the crash guard: when GNOME Shell fails within 60 seconds of the
layer's enable, apex-shell-safe.service sets layer-enabled to false for that user. The
light and dark Apex Facets wallpapers ship as PNGs, paired for GNOME's background
chooser. The Apex icon theme carries Colloid's full-colour app icons and the Apex
Symbolic glyphs, with their strokes turned into fills, and the flat Apex folders in blue
and its file icons, and inherits Adwaita and hicolor. Nine Apex-<accent> themes carry
the folders in each libadwaita accent and inherit Apex. The Plymouth script theme apex
draws the boot splash and the disk passphrase field at 1x and @2x; apex-twostep is its
two-step fallback. A tmpfiles entry creates the global Flatpak override, when there is
none, so that Flatpak apps read the window radius in apex.css.

%prep
%autosetup -n %{name}-%{version}
echo '%{colloid_sha256}  %{SOURCE1}' | sha256sum -c -
tar -xf %{SOURCE1}
cp -p Colloid-icon-theme-%{colloid_commit}/LICENSE LICENSE.Colloid

%build
# 3840x2400 covers the laptop's 2880x1800 panel and a 4K monitor.
rsvg-convert -w 3840 -h 2400 -o apex-facets-light.png desktop/wallpapers/apex-facets-light.svg
rsvg-convert -w 3840 -h 2400 -o apex-facets-dark.png desktop/wallpapers/apex-facets-dark.svg
rsvg-convert -w 2880 -h 1800 -o apex-greeter-light.png desktop/wallpapers/apex-greeter-light.svg
rsvg-convert -w 2880 -h 1800 -o apex-greeter-dark.png desktop/wallpapers/apex-greeter-dark.svg
bash desktop/gdm/build-logo.sh apex-gdm-logo.svg desktop/gdm/logo.svg %{fedora}
mkdir symbolic
for f in desktop/icons/symbolic/*.svg; do
    n=${f##*/}
    bash desktop/icons/fill-strokes.sh "$f" "symbolic/${n%.svg}-symbolic.svg"
done
bash desktop/icons/build-places.sh themes desktop/icons/places/folder.svg \
    desktop/icons/places/emblems desktop/icons/accents
bash desktop/icons/build-mimetypes.sh themes desktop/icons/mimetypes/file.svg \
    desktop/icons/mimetypes/kinds desktop/icons/mimetypes/types
bash desktop/plymouth/build.sh plymouth desktop/plymouth/art/*.svg

%install
install -Dm0644 desktop/schemas/io.github.apex_linux.Apex.Desktop.gschema.xml \
    %{buildroot}%{_datadir}/glib-2.0/schemas/io.github.apex_linux.Apex.Desktop.gschema.xml
install -Dm0644 desktop/systemd/user/apex-shell-safe.service \
    %{buildroot}%{_userunitdir}/apex-shell-safe.service
install -Dm0644 'desktop/systemd/user/org.gnome.Shell@.service.d/50-apex.conf' \
    '%{buildroot}%{_userunitdir}/org.gnome.Shell@.service.d/50-apex.conf'
install -Dm0644 desktop/systemd/user/apex-folder-icons.service \
    %{buildroot}%{_userunitdir}/apex-folder-icons.service
install -Dm0755 desktop/icons/apex-folder-icons.sh %{buildroot}%{_libexecdir}/apex-folder-icons
# Enabled for every user by this link, not by a preset: the spec runs no scriptlets.
install -dm0755 %{buildroot}%{_userunitdir}/graphical-session.target.wants
ln -s ../apex-folder-icons.service \
    %{buildroot}%{_userunitdir}/graphical-session.target.wants/apex-folder-icons.service
install -Dm0644 desktop/schemas/90_apex.gschema.override \
    %{buildroot}%{_datadir}/glib-2.0/schemas/90_apex.gschema.override
install -Dm0644 desktop/dconf/distro.d/50-apex-ptyxis \
    %{buildroot}%{_sysconfdir}/dconf/db/distro.d/50-apex-ptyxis
install -Dm0644 desktop/ptyxis/apex-prompt.sh %{buildroot}%{_sysconfdir}/profile.d/apex-prompt.sh
install -Dm0644 desktop/ptyxis/zz-apex-shell-status.sh \
    %{buildroot}%{_sysconfdir}/profile.d/zz-apex-shell-status.sh
install -Dm0644 desktop/tmpfiles/apex-desktop.conf %{buildroot}%{_tmpfilesdir}/apex-desktop.conf
install -Dm0644 desktop/keybindings/60-apex.xml \
    %{buildroot}%{_datadir}/gnome-control-center/keybindings/60-apex.xml
install -Dm0644 desktop/fontconfig/60-apex-adwaita-sans-ss03.conf \
    %{buildroot}%{_datadir}/fontconfig/conf.avail/60-apex-adwaita-sans-ss03.conf
install -dm0755 %{buildroot}%{_sysconfdir}/fonts/conf.d
ln -s ../../..%{_datadir}/fontconfig/conf.avail/60-apex-adwaita-sans-ss03.conf \
    %{buildroot}%{_sysconfdir}/fonts/conf.d/60-apex-adwaita-sans-ss03.conf
install -Dm0644 apex-facets-light.png %{buildroot}%{_datadir}/backgrounds/apex/apex-facets-light.png
install -Dm0644 apex-facets-dark.png %{buildroot}%{_datadir}/backgrounds/apex/apex-facets-dark.png
install -Dm0644 -t %{buildroot}%{_datadir}/backgrounds/apex apex-greeter-light.png apex-greeter-dark.png
install -Dm0644 apex-gdm-logo.svg %{buildroot}%{_datadir}/pixmaps/apex-gdm-logo.svg
install -Dm0644 desktop/gdm/zz_apex-login-screen.gschema.override \
    %{buildroot}%{_datadir}/glib-2.0/schemas/zz_apex-login-screen.gschema.override
install -Dm0644 desktop/wallpapers/apex-facets.xml \
    %{buildroot}%{_datadir}/gnome-background-properties/apex-facets.xml
install -Dm0644 desktop/icons/index.theme %{buildroot}%{_datadir}/icons/Apex/index.theme
install -Dm0644 -t %{buildroot}%{_datadir}/icons/Apex/symbolic symbolic/*-symbolic.svg
cp -a themes/Apex/. %{buildroot}%{_datadir}/icons/Apex/
cp -a themes/Apex-* %{buildroot}%{_datadir}/icons/
install -dm0755 %{buildroot}%{_datadir}/icons/Apex/scalable/apps
cp -a Colloid-icon-theme-%{colloid_commit}/src/apps/scalable/. \
    Colloid-icon-theme-%{colloid_commit}/links/apps/scalable/. \
    %{buildroot}%{_datadir}/icons/Apex/scalable/apps/
# Colloid links a few names to icons it does not ship, and one symbolic name to a colour icon.
find %{buildroot}%{_datadir}/icons/Apex/scalable/apps \( -xtype l -o -name '*-symbolic.svg' \) -print -delete
# Fedora's cache triggers cover only their own themes. GTK drops a cache older than its
# directory, and ostree commits both at mtime 0.
for t in %{buildroot}%{_datadir}/icons/Apex %{buildroot}%{_datadir}/icons/Apex-*; do
    gtk-update-icon-cache --force --quiet "$t"
done
install -Dm0644 -t %{buildroot}%{_datadir}/plymouth/themes/apex \
    desktop/plymouth/apex/apex.plymouth desktop/plymouth/apex/apex.script plymouth/apex/*.png
install -Dm0644 -t %{buildroot}%{_datadir}/plymouth/themes/apex-twostep \
    desktop/plymouth/apex-twostep/apex-twostep.plymouth plymouth/apex-twostep/*.png

%check
glib-compile-schemas --strict --dry-run %{buildroot}%{_datadir}/glib-2.0/schemas
bash desktop/icons/check-theme.sh %{buildroot}%{_datadir}/icons/Apex desktop/icons/symbolic
for t in %{buildroot}%{_datadir}/icons/Apex-*; do bash desktop/icons/check-theme.sh "$t"; done
bash desktop/icons/check-caches.sh %{buildroot}%{_datadir}/icons/Apex %{buildroot}%{_datadir}/icons/Apex-*
bash desktop/plymouth/check-theme.sh %{buildroot}%{_datadir}/plymouth/themes
bash desktop/wallpapers/check-greeter.sh %{buildroot}%{_datadir}/backgrounds/apex

%files
%license LICENSE
%license LICENSE.Colloid
%{_datadir}/glib-2.0/schemas/io.github.apex_linux.Apex.Desktop.gschema.xml
%{_datadir}/glib-2.0/schemas/90_apex.gschema.override
%{_datadir}/glib-2.0/schemas/zz_apex-login-screen.gschema.override
%{_datadir}/gnome-control-center/keybindings/60-apex.xml
%{_datadir}/fontconfig/conf.avail/60-apex-adwaita-sans-ss03.conf
%config(noreplace) %{_sysconfdir}/fonts/conf.d/60-apex-adwaita-sans-ss03.conf
%config(noreplace) %{_sysconfdir}/dconf/db/distro.d/50-apex-ptyxis
%config(noreplace) %{_sysconfdir}/profile.d/apex-prompt.sh
%config(noreplace) %{_sysconfdir}/profile.d/zz-apex-shell-status.sh
%{_userunitdir}/apex-shell-safe.service
%{_tmpfilesdir}/apex-desktop.conf
# gnome-shell ships no drop-in directory for its unit, so this package owns it.
%dir %{_userunitdir}/org.gnome.Shell@.service.d
%{_userunitdir}/org.gnome.Shell@.service.d/50-apex.conf
%{_userunitdir}/apex-folder-icons.service
%dir %{_userunitdir}/graphical-session.target.wants
%{_userunitdir}/graphical-session.target.wants/apex-folder-icons.service
%{_libexecdir}/apex-folder-icons
%dir %{_datadir}/backgrounds/apex
%{_datadir}/backgrounds/apex/apex-facets-light.png
%{_datadir}/backgrounds/apex/apex-facets-dark.png
%{_datadir}/backgrounds/apex/apex-greeter-light.png
%{_datadir}/backgrounds/apex/apex-greeter-dark.png
%{_datadir}/pixmaps/apex-gdm-logo.svg
%dir %{_datadir}/gnome-background-properties
%{_datadir}/gnome-background-properties/apex-facets.xml
%{_datadir}/icons/Apex/
%{_datadir}/icons/Apex-*/
%{_datadir}/plymouth/themes/apex/
%{_datadir}/plymouth/themes/apex-twostep/

%changelog
* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- folder-remote, a network mount's folder, in the accent with the network-wired emblem

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- A slides kind in GNOME Brown 3 for presentations, as boards 27 to 29 draw it: the generic
  x-office-presentation, and ODP, PPTX and PPT labelled

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- Board 31d's 72 Apex Symbolic glyphs (everywhere else): the last names Adwaita drew, and
  the shell's accessibility menu icon, so Apex Symbolic draws 268 of the 275 names

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- Board 31b's documents, shared and syncing emblems, which apps request and Adwaita 51
  does not draw

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- icon-theme.cache for Apex and the nine Apex-<accent> themes, built and validated here

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- Board 31c's 64 glyphs (the shell, OSDs, toolkit, Files and Settings fallbacks) and a
  filled starred beside board 31's outline, now non-starred

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- Board 31b's 69 glyphs: every Wi-Fi, battery, volume, microphone, Bluetooth,
  power-profile and VPN state the shell switches between, and the most visible
  gaps check-icons found (password reveal, clear, media, privacy indicators)

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- disabled-features takes only the layer's feature names, as choices, so gsettings refuses
  a misspelt one

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- apex-folder-icons.service: the Projects and Screenshots folder icons at login

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- Board 12's greeter: the pre-blurred Facets backgrounds at 2880x1800, and the gdm logo,
  the footer's wordmark and Fedora credit as paths, with its login-screen override

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- lower-refresh-rate-on-battery in the Apex schema: the panel's refresh rate on battery,
  which Settings' Power panel writes (board 24)

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- Apex file icons (boards 27 to 29): flat pages in board 27's file colours, labelled
  from 41 px up, for the generic icons and the common content types Files shows

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- zz-apex-shell-status.sh: a failed command reports its status to VTE, once, so the
  terminal can show it failed

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- search-hint-shown in the Apex schema: the shell shows "Press Super+Space to search"
  once

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- Apex folders (boards 27 to 29): flat, in the accent, with Apex Symbolic emblems
  from 33 px up; the nine Apex-<accent> folder themes, which inherit Apex

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- palette='apex' in the Apex Ptyxis profile, for apex-session-agent's accent palette
- tmpfiles: the global Flatpak override grants xdg-config/gtk-4.0:ro, so Flatpak
  apps read apex.css; created only when missing

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- /etc/profile.d/apex-prompt.sh: board 32's prompt, a blue directory and a dim $

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- Both Plymouth themes drawn for DeviceScale=1: apex-twostep at @2x with a 320x6 bar,
  and MonospaceFont=monospace 20 so the Esc view keeps its DeviceScale=2 size

* Sat Oct 24 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- The Plymouth script theme apex (boards 01 and 30): the wordmark, the 160x3 bar with
  round ends, the disk passphrase field, at 1x and @2x; apex-twostep as the fallback

* Fri Oct 23 2026 Thuong Vo <66083331+SekiroKenjii@users.noreply.github.com> - 0.1.0-0
- The 78 Apex Symbolic glyphs of board 31, filled by fill-strokes.sh at 100x scale

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
