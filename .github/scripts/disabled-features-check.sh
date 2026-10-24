#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Compiles the Apex schema and checks that disabled-features takes each of its choices, refuses
# a misspelt name, and that its description names exactly those choices.

set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

require glib-compile-schemas gsettings mktemp xmllint
xml=$APEX_ROOT/desktop/schemas/io.github.apex_linux.Apex.Desktop.gschema.xml
key='//key[@name="disabled-features"]'
mapfile -t choices < <(xmllint --xpath "$key/choices/choice/@value" "$xml" | sed 's/.*value="\(.*\)"/\1/')
((${#choices[@]} > 0)) || die "disabled-features has no choices"
described=$(xmllint --xpath "string($key/description)" "$xml" | tr -s ' \n' ' ' |
    sed -n 's/.*by name: \([^;]*\);.*/\1/p' | sed 's/,* and /, /' | tr -d ' ' | tr , '\n' | sort)
[[ $described == "$(printf '%s\n' "${choices[@]}" | sort)" ]] ||
    die "the disabled-features description names $(echo "$described" | paste -sd ' '), not its choices"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp "$xml" "$tmp/"
glib-compile-schemas --strict "$tmp"
export GSETTINGS_SCHEMA_DIR=$tmp GSETTINGS_BACKEND=memory
schema=io.github.apex_linux.Apex.Desktop
for c in "${choices[@]}"; do
    gsettings set "$schema" disabled-features "['$c']" || die "disabled-features refuses ['$c']"
done
gsettings set "$schema" disabled-features "['dock', 'glass']" || die "disabled-features refuses two choices"
if gsettings set "$schema" disabled-features "['dokc']" 2>/dev/null; then
    die "disabled-features takes ['dokc']"
fi
log "disabled-features-check.sh: disabled-features takes its ${#choices[@]} choices and refuses ['dokc']"
