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
# expected-symbolic.txt is make check-icons' input, not a file the RPM ships.
unpackaged=$(cd "$APEX_ROOT" && git ls-files --cached --others --exclude-standard -- desktop ':(exclude)desktop/README.md' \
    ':(exclude)desktop/icons/expected-symbolic.txt' |
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
    theme_fake && ln -s a.svg "$TMP/Apex/scalable/apps/e-symbolic.svg"
    check_false "check-theme.sh fails on a symbolic icon outside symbolic/" check_theme
    theme_fake && sed -i 's/fill="#000"/style="fill:#000;stroke-linecap:round;-inkscape-stroke:none"/' "$TMP/Apex/symbolic/c-symbolic.svg"
    check_true "check-theme.sh passes Inkscape's stroke-to-path output" check_theme
    theme_fake && sed -i 's/fill="#000"/style="fill:#000;stroke:#000"/' "$TMP/Apex/symbolic/c-symbolic.svg"
    check_false "check-theme.sh fails on a stroke in a style attribute" check_theme
    theme_fake && sed -i 's/fill="#000"/fill="#000" stroke="none" style="stroke:none"/' "$TMP/Apex/symbolic/c-symbolic.svg"
    check_true "check-theme.sh passes a stroke of none" check_theme
    mkdir -p "$TMP/src"
    printf '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0h1" stroke="#000" stroke-opacity=".35"/></svg>\n' >"$TMP/src/c.svg"
    check_opacity() { bash "$APEX_ROOT/desktop/icons/check-theme.sh" "$TMP/Apex" "$TMP/src"; }
    theme_fake && sed -i 's/fill="#000"/style="fill:#000;fill-opacity:0.35"/' "$TMP/Apex/symbolic/c-symbolic.svg"
    check_true "check-theme.sh passes a stroke-opacity that became a fill-opacity" check_opacity
    theme_fake
    check_false "check-theme.sh fails when a stroke-opacity is lost" check_opacity
    theme_fake && rm "$TMP/Apex/symbolic/c-symbolic.svg"
    check_false "check-theme.sh fails when a source has no symbolic output" check_opacity
fi

# --- fill-strokes.sh ------------------------------------------------------------------------
printf '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"/>\n' >"$TMP/big.svg"
check "fill-strokes.sh refuses a glyph off the 16 px grid" 1 \
    "$(rc_of bash "$APEX_ROOT/desktop/icons/fill-strokes.sh" "$TMP/big.svg" "$TMP/big-symbolic.svg")"
if command -v inkscape >/dev/null 2>&1; then
    printf '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><g stroke="#000" stroke-width="1.75" fill="none"><g><path d="M2 8h12"/></g></g></svg>\n' >"$TMP/g.svg"
    bash "$APEX_ROOT/desktop/icons/fill-strokes.sh" "$TMP/g.svg" "$TMP/g-symbolic.svg" >/dev/null 2>&1 || true
    check_true "fill-strokes.sh fills the strokes of a glyph nested two groups deep" \
        grep -Eq 'd="[Mm]' "$TMP/g-symbolic.svg"
    check_false "fill-strokes.sh leaves no stroke in a glyph nested two groups deep" \
        grep -Eq '(^|[^-[:alnum:]])stroke[[:space:]]*(=[[:space:]]*"|:)[[:space:]]*#' "$TMP/g-symbolic.svg"
fi

# --- apex-prompt.sh replaces only Fedora's default PS1, in interactive bash ------------------
# bash unsets PS1 when it starts non-interactive, so each run sets it after startup.
cat >"$TMP/prompt.sh" <<'EOF'
PS1=$2
. "$1"
printf '%s' "$PS1"
EOF
prompt_in() {
    local flags=$1 ps1=$2
    shift 2
    env -i HOME="$TMP" "$@" bash --norc --noprofile "$flags" "$TMP/prompt.sh" \
        "$APEX_ROOT/desktop/ptyxis/apex-prompt.sh" "$ps1" 2>/dev/null
}
prompt_of() { prompt_in -i "$@"; }
readonly FEDORA_PS1='[\u@\h \W]\$ '
check "the prompt is a blue directory and a dim \$" '\[\e[34m\]\w\[\e[0;2m\] \$\[\e[0m\] ' \
    "$(prompt_of "$FEDORA_PS1")"
check "bash's own default PS1 gets the same prompt" "$(prompt_of "$FEDORA_PS1")" "$(prompt_of '\s-\v\$ ')"
check "over SSH, user@host in green comes first" \
    '\[\e[32m\]\u@\h\[\e[0;2m\]:\[\e[0;34m\]\w\[\e[0;2m\]\$\[\e[0m\] ' \
    "$(prompt_of "$FEDORA_PS1" SSH_CONNECTION='10.0.0.2 5 10.0.0.1 22')"
check "a PS1 that is not a default stays" '> ' "$(prompt_of '> ')"
check "apex_prompt_disable keeps Fedora's prompt" "$FEDORA_PS1" "$(prompt_of "$FEDORA_PS1" apex_prompt_disable=1)"
check "NO_COLOR keeps Fedora's prompt" "$FEDORA_PS1" "$(prompt_of "$FEDORA_PS1" NO_COLOR=1)"
check "a non-interactive bash keeps its PS1" "$FEDORA_PS1" \
    "$(prompt_in +i "$FEDORA_PS1")"
check_true "a POSIX sh parses apex-prompt.sh" sh "$APEX_ROOT/desktop/ptyxis/apex-prompt.sh"

# --- .gitignore: biometric data never gets tracked --------------------------------------
for f in a.pgm B.PGM x/print.Variant rec.ioctl x/y/rec.UMOCKDEV cap.pcap cap.PcapNG var/lib/fprint/u/1; do
    check_true ".gitignore ignores $f" git -C "$APEX_ROOT" check-ignore -q --no-index "$f"
done
check_false ".gitignore keeps the dconf keyfiles" \
    git -C "$APEX_ROOT" check-ignore -q --no-index desktop/dconf/distro.d/50-apex-ptyxis

# --- tools/icons/scan.sh, over a fake rpm -----------------------------------------------------
mkdir -p "$TMP/scan/bin" "$TMP/scan/pkg/icons/hicolor/symbolic/apps"
# shellcheck disable=SC2016 # the shell template is the input, not an expansion
printf '%s\n' "label='x-symbolic' y@2-symbolic view-%s-symbolic" '`net-${s}-symbolic` z-symbolic' \
    'Clipboardexternal-link-symbolic image.dialog-error-symbolic org.gnome.Fake-symbolic force-symbolic' \
    "'w-symbolic' /org/fake/icons/scalable/actions/w-symbolic.svg" >"$TMP/scan/pkg/a.js"
: >"$TMP/scan/pkg/icons/hicolor/symbolic/apps/z-symbolic.svg"
cat >"$TMP/scan/bin/rpm" <<FAKE
#!/bin/sh
case "\$1" in -ql) printf '%s\n' "$TMP/scan/pkg/a.js" "$TMP/scan/pkg/icons/hicolor/symbolic/apps/z-symbolic.svg" ;;
    -qa) echo 'fake fake-1-1.src.rpm' ;;
    -q) case "\$3" in *SOURCERPM*) printf 'fake-1-1.src.rpm' ;; *NAME*) echo '@fake-1-1' ;; esac ;; esac
exit 0
FAKE
printf '#!/bin/sh\nexit 1\n' >"$TMP/scan/bin/gresource"
chmod +x "$TMP/scan/bin/rpm" "$TMP/scan/bin/gresource"
printf 'fake\n' >"$TMP/scan/packages"
scanned=$(PATH="$TMP/scan/bin:$PATH" bash "$APEX_ROOT/tools/icons/scan.sh" "$TMP/scan/packages" 2>"$TMP/scan/templates" |
    grep -v -e '^[#@]' -e $'\tgnome-shell$')
check "scan.sh lists literal names and app ids, not a name the package ships, a fragment or a run-together string" \
    "$(printf 'org.gnome.Fake-symbolic\tfake\nx-symbolic\tfake')" "$scanned"
check_true "scan.sh reports a name built at run time" grep -Fq 'template fake: view-%s-symbolic' "$TMP/scan/templates"

# --- symbolic-check.py, where GTK 4 for Python is installed ------------------------------------
if python3 -c 'import gi; gi.require_version("Gtk", "4.0"); from gi.repository import Gtk' 2>/dev/null; then
    mkdir -p "$TMP/sym/themes/Apex/symbolic" "$TMP/sym/share/Adwaita/symbolic/actions" "$TMP/sym/share/hicolor"
    cp "$APEX_ROOT/desktop/icons/index.theme" "$TMP/sym/themes/Apex/"
    printf '[Icon Theme]\nName=Adwaita\nInherits=hicolor\nDirectories=symbolic/actions\n[symbolic/actions]\nSize=16\nMinSize=8\nMaxSize=512\nType=Scalable\n' \
        >"$TMP/sym/share/Adwaita/index.theme"
    printf '[Icon Theme]\nName=Hicolor\nDirectories=\n' >"$TMP/sym/share/hicolor/index.theme"
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"><path d="M0 0h16v16z"/></svg>'
    printf '%s\n' "$svg" >"$TMP/sym/themes/Apex/symbolic/apex-only-symbolic.svg"
    printf '%s\n' "$svg" >"$TMP/sym/share/Adwaita/symbolic/actions/stock-only-symbolic.svg"
    printf '# list\n@fake-1-1\napex-only-symbolic\tfake\nstock-only-symbolic\tfake\n' >"$TMP/sym/names"
    sym_check() { python3 "$APEX_ROOT/.github/scripts/symbolic-check.py" "$TMP/sym/names" "$TMP/sym/themes" --search "$TMP/sym/share" \
        ${sym_gaps:+--unresolved "$sym_gaps"}; }
    sym_gaps=
    check "symbolic-check.py counts an Apex glyph and an Adwaita fallback" \
        "symbolic-check.py: 2 names: 1 from Apex, 1 from Adwaita" "$(sym_check 2>&1)"
    printf 'toolkit-only-symbolic\tfake\ttoolkit\n' >>"$TMP/sym/names"
    check_true "symbolic-check.py counts a name its toolkit bundles" sym_check
    printf 'apex-no-such-icon-symbolic\tfake\n' >>"$TMP/sym/names"
    check_false "symbolic-check.py fails on a name nothing draws" sym_check
    printf 'apex-no-such-icon-symbolic\tstock draws none\n' >"$TMP/sym/gaps"
    sym_gaps=$TMP/sym/gaps
    check_true "symbolic-check.py passes a listed gap" sym_check
    printf 'stock-only-symbolic\tstale\n' >>"$TMP/sym/gaps"
    check_false "symbolic-check.py fails on a listed gap that resolves" sym_check
fi
# --- apex-folder-icons.sh, against a temporary HOME -------------------------------------------
mkdir -p "$TMP/fi/bin"
cat >"$TMP/fi/bin/gio" <<'FAKE'
#!/bin/sh
case "$1" in
    info) [ -e "$4/.fake-icon" ] && echo '  metadata::custom-icon-name: user-set'; exit 0 ;;
    set) echo "$4 $5 $6" >>"$HOME/gio.log" ;;
esac
FAKE
# shellcheck disable=SC2016 # the fakes expand these when they run
{
    printf '#!/bin/sh\necho "$HOME/Pictures"\n' >"$TMP/fi/bin/xdg-user-dir"
    printf '#!/bin/sh\necho "${FAKE_SHOTS:-Screenshots}"\n' >"$TMP/fi/bin/gettext"
}
chmod +x "$TMP/fi/bin/"*
folder_icons() {
    rm -rf "$TMP/fi/home" && mkdir -p "$TMP/fi/home"
    for d in "$@"; do mkdir -p "$TMP/fi/home/$d"; done
    HOME="$TMP/fi/home" PATH="$TMP/fi/bin:$PATH" sh "$APEX_ROOT/desktop/icons/apex-folder-icons.sh"
    cat "$TMP/fi/home/gio.log" 2>/dev/null || true
}
check "apex-folder-icons.sh sets both icons when both folders exist" \
    "$TMP/fi/home/Projects metadata::custom-icon-name folder-projects
$TMP/fi/home/Pictures/Screenshots metadata::custom-icon-name folder-screenshots" \
    "$(folder_icons Projects Pictures/Screenshots)"
check "apex-folder-icons.sh sets nothing when the folders are absent" "" "$(folder_icons Pictures)"
check_false "apex-folder-icons.sh creates no folder" test -e "$TMP/fi/home/Projects"
check "apex-folder-icons.sh keeps an icon the user set" \
    "$TMP/fi/home/Pictures/Screenshots metadata::custom-icon-name folder-screenshots" \
    "$(folder_icons Projects/.fake-icon Pictures/Screenshots)"
check "apex-folder-icons.sh finds Screenshots under the shell's translation" \
    "$TMP/fi/home/Pictures/Ảnh chụp màn hình metadata::custom-icon-name folder-screenshots" \
    "$(FAKE_SHOTS='Ảnh chụp màn hình' folder_icons 'Pictures/Ảnh chụp màn hình' Pictures/Screenshots)"

if ((FAILS > 0)); then
    die "selftest: $FAILS failure(s)"
fi
log "selftest: all $TESTS checks passed"
