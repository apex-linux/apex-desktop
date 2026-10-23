#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Against fakes only: no network, no root.

set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

require awk sed git sha256sum mktemp

FAILS=0
TESTS=0
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

pass() { TESTS=$((TESTS + 1)); }
flunk() {
    TESTS=$((TESTS + 1))
    FAILS=$((FAILS + 1))
    printf 'FAIL: %s\n' "$*" >&2
}

check() {
    local name=$1 expected=$2 actual=$3
    if [[ $expected == "$actual" ]]; then pass; else flunk "$name: expected '$expected', got '$actual'"; fi
}

check_true() {
    local name=$1
    shift
    if (set +e; "$@") >/dev/null 2>&1; then pass; else flunk "$name: expected success"; fi
}
check_false() {
    local name=$1
    shift
    if (set +e; "$@") >/dev/null 2>&1; then flunk "$name: expected failure"; else pass; fi
}

rc_of() { local rc=0; "$@" >/dev/null 2>&1 || rc=$?; printf '%s' "$rc"; }
rpms_fn() { bash -c '. "$1"; shift; "$@"' _ "$APEX_ROOT/.github/scripts/rpms.sh" "$@"; }

# --- rpms.sh: the apex-desktop key ----------------------------------------------------------
check "the key covers desktop/, the spec, the Makefile and LICENSE" \
    "desktop packaging/apex-desktop.spec Makefile LICENSE" \
    "$(bash -c '. "$1"; printf "%s\n" "${KEY_PATHS[*]}"' _ "$APEX_ROOT/.github/scripts/rpms.sh")"
readonly RECIPE_A=$'repos --repo=fedora --repo=updates\n100755 blob 1111\t.github/scripts/rpms.sh'
key=$(rpms_fn key_of "$RECIPE_A" "tree")
check "a key is 64 hex digits" 64 "$(tr -dc '0-9a-f' <<<"$key" | wc -c)"
check "the same inputs give the same key" "$key" "$(rpms_fn key_of "$RECIPE_A" "tree")"
check_false "a desktop change changes the key" test "$key" = "$(rpms_fn key_of "$RECIPE_A" "tree2")"
check_false "a recipe change changes the key" test "$key" = "$(rpms_fn key_of "${RECIPE_A/1111/2222}" "tree")"
check_true "the key of this checkout is 64 hex digits" \
    grep -Eqx '[0-9a-f]{64}' <<<"$("$APEX_ROOT/.github/scripts/rpms.sh" key 2>/dev/null)"
check "rpms.sh with no command prints its usage and exits 2" 2 "$(rc_of "$APEX_ROOT/.github/scripts/rpms.sh")"
if ((EUID != 0)); then
    check "rpms.sh build refuses to run as a user" 1 "$(rc_of "$APEX_ROOT/.github/scripts/rpms.sh" build "$TMP/rpms")"
fi

# --- apex-desktop.spec installs every file of desktop/ ---------------------------------------
unpackaged=$(cd "$APEX_ROOT" && git ls-files --cached --others --exclude-standard -- desktop ':(exclude)desktop/README.md' |
    while IFS= read -r f; do
        grep -Fq -e "$f" -e "${f%/*}/*.${f##*.}" packaging/apex-desktop.spec || printf '%s ' "$f"
    done)
check "apex-desktop.spec installs every desktop/ file" "" "$unpackaged"
misplaced=$(awk '/^%install/ {s = 1; next} /^%(check|files|changelog)/ {s = 0} s && /^%(config|dir|license|doc)/' \
    "$APEX_ROOT/packaging/apex-desktop.spec")
check "apex-desktop.spec's %install holds no %files directive" "" "$misplaced"
files_section=$(awk '/^%files/ {s = 1; next} /^%changelog/ {s = 0} s' "$APEX_ROOT/packaging/apex-desktop.spec")
for line in '%license LICENSE.Colloid' '%{_datadir}/icons/Apex/'; do
    check_true "apex-desktop.spec's %files lists $line" grep -Fxq -- "$line" <<<"$files_section"
done

# --- The Colloid pin is a key input -------------------------------------------------------
spec_global() { sed -n "s/^%global $1[[:space:]]*//p" "$APEX_ROOT/packaging/apex-desktop.spec"; }
check_true "the spec pins a Colloid commit" grep -Eqx '[0-9a-f]{40}' <<<"$(spec_global colloid_commit)"
check_true "the spec pins Colloid's SHA-256" grep -Eqx '[0-9a-f]{64}' <<<"$(spec_global colloid_sha256)"
check_true "%prep checks the Colloid source's SHA-256 before unpacking it" \
    awk '/^%prep/ {p = 1} p && /sha256sum -c/ {c = NR} p && /tar -xf %\{SOURCE1\}/ {t = NR} END {exit !(c && t > c)}' \
    "$APEX_ROOT/packaging/apex-desktop.spec"
check_true "make rpm fetches the commit the spec pins" \
    grep -Fq -- "fetch -q --depth 1 'https://github.com/vinceliuice/Colloid-icon-theme.git' '$(spec_global colloid_commit)'" \
    <<<"$(make -s -n -C "$APEX_ROOT" rpm 2>/dev/null)"

# --- icon-theme='Apex' ships with a theme that inherits Adwaita ------------------------------
check "the override sets icon-theme='Apex'" "icon-theme='Apex'" \
    "$(grep -x "icon-theme=.*" "$APEX_ROOT/desktop/schemas/90_apex.gschema.override")"
check "desktop/icons/index.theme names the Apex theme" "Name=Apex" "$(grep -x 'Name=.*' "$APEX_ROOT/desktop/icons/index.theme")"

# --- check-theme.sh -------------------------------------------------------------------------
if command -v xmllint >/dev/null 2>&1; then
    theme_fake() {
        rm -rf "$TMP/Apex" && mkdir -p "$TMP/Apex/scalable/apps" "$TMP/Apex/symbolic"
        cp "$APEX_ROOT/desktop/icons/index.theme" "$TMP/Apex/"
        printf '<svg xmlns="http://www.w3.org/2000/svg"><path fill="#000" d="M0 0h1v1z"/></svg>\n' >"$TMP/Apex/scalable/apps/a.svg"
        ln -s a.svg "$TMP/Apex/scalable/apps/b.svg"
        cp "$TMP/Apex/scalable/apps/a.svg" "$TMP/Apex/symbolic/c-symbolic.svg"
    }
    check_theme() { bash "$APEX_ROOT/desktop/icons/check-theme.sh" "$TMP/Apex"; }
    theme_fake
    check_true "check-theme.sh passes a good theme" check_theme
    theme_fake && sed -i 's/^Inherits=.*/Inherits=hicolor/' "$TMP/Apex/index.theme"
    check_false "check-theme.sh fails without Adwaita in Inherits" check_theme
    theme_fake && sed -i 's/^Directories=.*/Directories=symbolic/' "$TMP/Apex/index.theme"
    check_false "check-theme.sh fails on icons in an unlisted directory" check_theme
    theme_fake && sed -i '/^\[symbolic\]/,$ s/^Size=.*/Size=big/' "$TMP/Apex/index.theme"
    check_false "check-theme.sh fails on a Size that is not an integer" check_theme
    theme_fake && printf '<svg>\n' >"$TMP/Apex/scalable/apps/a.svg"
    check_false "check-theme.sh fails on an SVG that does not parse" check_theme
    theme_fake && ln -s gone.svg "$TMP/Apex/scalable/apps/d.svg"
    check_false "check-theme.sh fails on a dangling link" check_theme
    theme_fake && sed -i 's/fill="#000"/fill="none" stroke="#000"/' "$TMP/Apex/symbolic/c-symbolic.svg"
    check_false "check-theme.sh fails on a symbolic icon with a stroke" check_theme
fi

# --- .gitignore: biometric data never gets tracked --------------------------------------
for f in a.pgm B.PGM x/print.Variant rec.ioctl x/y/rec.UMOCKDEV cap.pcap cap.PcapNG var/lib/fprint/u/1; do
    check_true ".gitignore ignores $f" git -C "$APEX_ROOT" check-ignore -q --no-index "$f"
done
check_false ".gitignore keeps the dconf keyfiles" \
    git -C "$APEX_ROOT" check-ignore -q --no-index desktop/dconf/distro.d/50-apex-ptyxis

if ((FAILS > 0)); then
    die "selftest: $FAILS failure(s)"
fi
log "selftest: all $TESTS checks passed"
