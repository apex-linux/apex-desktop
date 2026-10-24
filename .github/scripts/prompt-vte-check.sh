#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Runs Fedora's /etc/bashrc as Ptyxis starts it, with apex-prompt.sh among the real
# /etc/profile.d scripts, and checks that VTE's shell integration still wraps our prompt.

set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

[[ $EUID -eq 0 && ( -e /.dockerenv || -e /run/.containerenv ) ]] ||
    die "prompt-vte-check.sh installs into /etc/profile.d; run it as root in a throwaway container"
[[ -f /etc/profile.d/vte.sh && -f /etc/bashrc ]] || die "needs /etc/profile.d/vte.sh (Fedora: vte-profile) and /etc/bashrc"

target=/etc/profile.d/apex-prompt.sh
[[ ! -e $target ]] || die "$target already exists"
tmp=$(mktemp -d)
install -m0644 "$APEX_ROOT/desktop/ptyxis/apex-prompt.sh" "$target"
trap 'rm -f "$target"; rm -rf "$tmp"' EXIT

fails=0
fail() {
    printf 'FAIL: %s\n' "$*" >&2
    fails=$((fails + 1))
}

cat >"$tmp/order.sh" <<'SH'
for f in /etc/profile.d/*.sh; do echo "${f##*/}"; done
SH
cat >"$tmp/state.sh" <<'SH'
printf '%s\n' "$PS1"
declare -p PROMPT_COMMAND
declare -F __vte_prompt_command __vte_precmd || true
SH
cat >"$tmp/alone.sh" <<'SH'
PS1='[\u@\h \W]\$ '
. "$1"
printf '%s' "$PS1"
SH

# /etc/bashrc sources the scripts in its glob's order; vte.sh skips a PS1 that has 133 already.
order=$(bash "$tmp/order.sh")
apex_at=$(grep -nx apex-prompt.sh <<<"$order" | cut -d: -f1)
vte_at=$(grep -nx vte.sh <<<"$order" | cut -d: -f1)
((apex_at < vte_at)) || fail "apex-prompt.sh sorts after vte.sh: $(tr '\n' ' ' <<<"$order")"

apex_ps1=$(env -i bash --norc --noprofile -i "$tmp/alone.sh" "$target" 2>/dev/null)
[[ $apex_ps1 == *'\[\e[34m\]\w'* ]] || fail "apex-prompt.sh gave '$apex_ps1' on Fedora's default PS1"
expected='\[\e]133;D;$?\e\\\e]133;A\e\\\]'"$apex_ps1"'\[\e]133;B\e\\\]'

state=$(env -i HOME=/nonexistent TERM=xterm-256color COLORTERM=truecolor VTE_VERSION=8401 \
    USER=apex DESKTOP_SESSION=gnome bash --rcfile /etc/bashrc -i "$tmp/state.sh" 2>/dev/null)
ps1=$(head -n 1 <<<"$state")
[[ $ps1 == "$expected" ]] || fail "PS1 is not ours inside VTE's OSC 133 D;A and B markers:
  got      $ps1
  expected $expected"
grep -q '^declare .*PROMPT_COMMAND=.*__vte_\(prompt_command\|precmd\)' <<<"$state" ||
    fail "PROMPT_COMMAND does not run VTE's prompt command: $(grep PROMPT_COMMAND <<<"$state" || true)"
grep -qx '__vte_\(prompt_command\|precmd\)' <<<"$state" || fail "vte.sh's prompt functions are not defined"

((fails == 0)) || exit 1
log "prompt-vte-check.sh: VTE's OSC 133 markers wrap the Apex prompt, and PROMPT_COMMAND runs $(grep -x '__vte_.*' <<<"$state" | head -n 1)"
