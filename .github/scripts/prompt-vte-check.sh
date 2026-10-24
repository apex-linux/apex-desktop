#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Runs Fedora's /etc/bashrc as Ptyxis starts it, with apex-prompt.sh and zz-apex-shell-status.sh
# among the real /etc/profile.d scripts, and checks VTE's shell integration around them.

set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

[[ $EUID -eq 0 && ( -e /.dockerenv || -e /run/.containerenv ) ]] ||
    die "prompt-vte-check.sh installs into /etc/profile.d; run it as root in a throwaway container"
[[ -f /etc/profile.d/vte.sh && -f /etc/bashrc ]] || die "needs /etc/profile.d/vte.sh (Fedora: vte-profile) and /etc/bashrc"

require script
target=/etc/profile.d/apex-prompt.sh status_sh=/etc/profile.d/zz-apex-shell-status.sh
for f in "$target" "$status_sh"; do
    [[ ! -e $f ]] || die "$f already exists"
done
tmp=$(mktemp -d)
install -m0644 "$APEX_ROOT/desktop/ptyxis/apex-prompt.sh" "$target"
install -m0644 "$APEX_ROOT/desktop/ptyxis/zz-apex-shell-status.sh" "$status_sh"
trap 'rm -f "$target" "$status_sh"; rm -rf "$tmp"' EXIT

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
status_at=$(grep -nx zz-apex-shell-status.sh <<<"$order" | cut -d: -f1)
((status_at > vte_at)) || fail "zz-apex-shell-status.sh sorts before vte.sh, so vte.sh would undo it"

# zz-apex-shell-status.sh replaces this function; a VTE update that changes it must fail here.
cat >"$tmp/vte_precmd" <<'SH'
__vte_precmd ()
{
    local errsv="$?";
    __vte_termprop_set "vte.shell.postexec" "$?";
    __vte_termprop_signal "vte.shell.precmd";
    return $errsv
}
SH
vte_precmd=$(env -i TERM=xterm-256color VTE_VERSION=8401 bash --norc --noprofile -i \
    -c '. /etc/profile.d/vte.sh; declare -f __vte_precmd' 2>/dev/null | sed 's/[[:space:]]*$//')
[[ $vte_precmd == "$(<"$tmp/vte_precmd")" ]] ||
    fail "vte.sh's __vte_precmd is not the one zz-apex-shell-status.sh replaces:
$vte_precmd"

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

# false, true, an empty line, (exit 3): each status once, after the command's preexec.
want='666;vte.shell.precmd! 133;D;0 133;A 133;B'
want+=' 133;C 666;vte.shell.preexec! 666;vte.shell.postexec=1 666;vte.shell.precmd! 133;D;1 133;A 133;B'
want+=' 133;C 666;vte.shell.preexec! 666;vte.shell.postexec=0 666;vte.shell.precmd! 133;D;0 133;A 133;B'
want+=' 666;vte.shell.precmd! 133;D;0 133;A 133;B'
want+=' 133;C 666;vte.shell.preexec! 666;vte.shell.postexec=3 666;vte.shell.precmd! 133;D;3 133;A 133;B'
want+=' 133;C 666;vte.shell.preexec!'
got=$(printf 'false\ntrue\n\n(exit 3)\nexit\n' |
    env -i HOME=/nonexistent TERM=xterm-256color VTE_VERSION=8401 USER=apex PATH=/usr/bin:/bin \
        script -q -c 'bash --rcfile /etc/bashrc -i' /dev/null |
    grep -ao $'\e\\]\\(666\\|133\\);[^\e]*' | sed 's/^\x1b\]//' | tr '\n' ' ' | sed 's/ $//')
[[ $got == "$want" ]] || fail "the shell's OSC 666 and 133 sequences differ:
  got      $got
  expected $want"

((fails == 0)) || exit 1
log "prompt-vte-check.sh: VTE's OSC 133 markers wrap the Apex prompt, and each command reports its own status once"
