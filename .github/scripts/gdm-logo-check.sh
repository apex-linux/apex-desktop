#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Compiles org.gnome.login-screen with Fedora gdm's override and Apex's, and checks that the
# logo key reads Apex's logo: overrides apply in lexical order, so the later name must win.

set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

require glib-compile-schemas gsettings mktemp
apex=$APEX_ROOT/desktop/gdm/zz_apex-login-screen.gschema.override
want=$(sed -n "s/^logo=//p" "$apex")
[[ $want == "'/usr/share/pixmaps/apex-gdm-logo.svg'" ]] || die "$apex sets logo=$want"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
real=/usr/share/glib-2.0/schemas/org.gnome.login-screen.gschema.xml
if [[ -f $real ]]; then
    cp "$real" /usr/share/glib-2.0/schemas/org.gnome.login-screen.gschema.override "$tmp/"
    source="gdm's own schema and override"
else
    cat >"$tmp/org.gnome.login-screen.gschema.xml" <<'XML'
<schemalist>
  <schema id="org.gnome.login-screen" path="/org/gnome/login-screen/">
    <key name="logo" type="s"><default>''</default></key>
  </schema>
</schemalist>
XML
    printf '[org.gnome.login-screen]\nlogo=%s\n' "'/usr/share/pixmaps/fedora-gdm-logo.png'" \
        >"$tmp/org.gnome.login-screen.gschema.override"
    source="a stand-in for gdm 51's schema and override (gdm is not installed)"
fi
cp "$apex" "$tmp/"
glib-compile-schemas --strict "$tmp"
got=$(gsettings --schemadir "$tmp" get org.gnome.login-screen logo)
[[ $got == "$want" ]] || die "org.gnome.login-screen logo is $got, not $want, with $source"
log "gdm-logo-check.sh: org.gnome.login-screen logo reads $got, with $source"
