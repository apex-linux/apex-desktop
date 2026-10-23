#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

usage() {
    cat >&2 <<'EOF'

Content key and build of the apex-desktop RPM. `build` runs inside
registry.fedoraproject.org/fedora:45 as root, from Fedora's fedora and updates
repositories.

  rpms.sh key                  print the content key of the apex-desktop RPM for git HEAD
  rpms.sh build OUTDIR [KEY]   install build deps, `make rpm`, copy the binary RPM to
                               OUTDIR with its key (KEY); with KEY, fail if the key
                               changed meanwhile
EOF
    exit 2
}

# Bump a schema when the inputs or the format of its key change.
readonly KEY_SCHEMA=2
# LICENSE is the RPM's %license.
readonly KEY_PATHS=(desktop packaging/apex-desktop.spec Makefile LICENSE)
readonly RECIPE_PATHS=(.github/scripts/rpms.sh)
readonly SPEC="$APEX_ROOT/packaging/apex-desktop.spec"
readonly COMPOSE_REPOS=(--repo=fedora --repo=updates)

git_() { git -c safe.directory="$APEX_ROOT" -C "$APEX_ROOT" "$@"; }

key_of() {
    {
        printf 'apex-desktop key schema %s\n' "$KEY_SCHEMA"
        printf 'recipe %s\n' "$1"
        printf '%s\n' "$2"
    } | sha256sum | cut -c1-64
}

committed() {
    local p
    for p in "$@"; do
        git_ cat-file -e "HEAD:$p" 2>/dev/null ||
            die "$p is not committed at HEAD; the RPM key covers committed files only"
    done
}

recipe() {
    committed "${RECIPE_PATHS[@]}"
    printf 'repos %s\n' "${COMPOSE_REPOS[*]}"
    git_ ls-tree HEAD -- "${RECIPE_PATHS[@]}"
}

desktop_tree() {
    committed "${KEY_PATHS[@]}"
    git_ ls-tree -r HEAD -- "${KEY_PATHS[@]}"
}

compute_key() {
    local tree rec
    # One assignment each, so a failing $(...) stops the script instead of shortening the key's input.
    tree=$(desktop_tree)
    rec=$(recipe)
    key_of "$rec" "$tree"
}

cmd_key() {
    (($# == 0)) || die "usage: rpms.sh key"
    require git sha256sum
    compute_key
}

# The Makefile runs git, and a checkout owned by another uid (a bind mount into a rootful
# container) needs safe.directory; this sets it for the one command, in no gitconfig file.
make_in_checkout() {
    GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0="$APEX_ROOT" \
        make -C "$APEX_ROOT" "$@"
}

cmd_build() {
    (($# >= 1 && $# <= 2)) || die "usage: rpms.sh build OUTDIR [KEY]"
    local outdir=$1 expected=${2:-}
    ((EUID == 0)) || die "rpms.sh build installs packages; run it as root in a fedora:45 container"
    require dnf5

    group "Build dependencies (${COMPOSE_REPOS[*]})"
    retry 3 10 dnf5 -y --setopt=install_weak_deps=False "${COMPOSE_REPOS[@]}" install \
        dnf5-plugins rpm-build make git-core findutils tar gzip
    retry 3 10 dnf5 -y --setopt=install_weak_deps=False "${COMPOSE_REPOS[@]}" builddep "$SPEC"
    endgroup

    local key
    key=$(compute_key)
    if [[ -n $expected && $key != "$expected" ]]; then
        die "content key changed between resolve and build ($expected -> $key)"
    fi

    group "make rpm"
    # A reused checkout must never ship an RPM left over from an earlier build.
    rm -rf "$APEX_ROOT/target/rpm"
    make_in_checkout rpm
    endgroup

    mkdir -p "$outdir"
    local -a rpms
    mapfile -t rpms < <(find "$APEX_ROOT/target/rpm/RPMS" -type f -name 'apex-desktop-*.rpm' | sort)
    ((${#rpms[@]} == 1)) || die "make rpm produced ${#rpms[@]} apex-desktop RPMs under target/rpm/RPMS, not one"
    cp -- "${rpms[@]}" "$outdir/"
    (cd "$outdir" && sha256sum -- *.rpm >SHA256SUMS)
    printf '%s\n' "$key" >"$outdir/KEY"

    summary "### apex-desktop RPM" "" "Key \`$key\`" "" '```' "$(cd "$outdir" && cat SHA256SUMS)" '```'
    log "built ${rpms[0]##*/} into $outdir"
}

main() {
    local cmd=${1:-}
    shift || true
    case $cmd in
        key) cmd_key "$@" ;;
        build) cmd_build "$@" ;;
        *) usage ;;
    esac
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
    main "$@"
fi
