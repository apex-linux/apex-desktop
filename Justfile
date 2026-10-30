# SPDX-License-Identifier: GPL-3.0-or-later

set shell := ["bash", "-euo", "pipefail", "-c"]

# List the recipes.
default:
    @just --list

# The data checks, the script self-test and the comment guard, as ci.yml runs them (checks whose tool is missing skip).
check: check-data selftest
    apex-lint comments

# xmllint, glib-compile-schemas --strict and dconf compile on desktop/.
check-data:
    make check-data

# The script self-tests, as ci.yml runs them.
selftest:
    .github/scripts/selftest.sh

# Board 31's contact sheets, every Apex Symbolic glyph as GTK 4 draws it, from an icons dir into OUT.
contact-sheet icons="/usr/share/icons" out="target/contact-sheet":
    tools/icons/contact-sheet.sh {{icons}} {{out}}

# The apex-desktop RPM from git HEAD (Fedora only: the builder VM or a fedora:45 toolbox).
rpm:
    make rpm

# The comment guard on every tracked file, or on the given ones (cargo install --git https://github.com/apex-linux/apex-ci apex-lint).
[positional-arguments]
lint-comments *paths:
    apex-lint comments "$@"
