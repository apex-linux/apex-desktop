# SPDX-License-Identifier: GPL-3.0-or-later
#
# vte.sh's __vte_precmd reports a status after PROMPT_COMMAND's earlier entries reset $?, so
# a failed command reads as 0. This reports the real status first, and only after a command.

# shellcheck shell=bash
[ -n "${BASH_VERSION-}" ] || return 0
case $- in *i*) ;; *) return 0 ;; esac
[[ $(type -t __vte_precmd) == function && $(declare -p PROMPT_COMMAND 2>/dev/null) == "declare -a"* ]] ||
    return 0

__apex_postexec() {
    local status=$?
    if [[ -n ${__apex_command_ran-} ]]; then
        __apex_command_ran=
        printf '\e]666;vte.shell.postexec=%s\e\134' "$status"
    fi
    return "$status"
}

__vte_precmd() {
    __vte_termprop_signal "vte.shell.precmd"
}

PROMPT_COMMAND=(__apex_postexec "${PROMPT_COMMAND[@]}")
# Bash expands PS0 only before running a command, and an assignment there stays set.
# shellcheck disable=SC2016
PS0='${BASH_VERSION:$((__apex_command_ran = 1, 0)):0}'"${PS0-}"
