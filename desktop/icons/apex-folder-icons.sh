#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
#
# apex-folder-icons.service runs it at each login: board 27's emblems for two folders GLib
# gives no special icon. It never creates a folder or replaces an icon the user chose.

set -u

set_icon() {
    [ -d "$1" ] || return 0
    info=$(gio info -a metadata::custom-icon-name,metadata::custom-icon "$1" 2>/dev/null) || return 0
    case $info in *metadata::custom-icon*) return 0 ;; esac
    gio set -t string "$1" metadata::custom-icon-name "$2"
}

set_icon "$HOME/Projects" folder-projects

pictures=$(xdg-user-dir PICTURES 2>/dev/null) || pictures=
[ -n "$pictures" ] || pictures=$HOME
# GNOME Shell saves screenshots in Pictures under its own translation of "Screenshots".
shots=$(gettext -d gnome-shell Screenshots 2>/dev/null) || shots=
[ -n "$shots" ] || shots=Screenshots
# A Screenshots folder the shell creates during a session gets its icon at the next login.
set_icon "$pictures/$shots" folder-screenshots
