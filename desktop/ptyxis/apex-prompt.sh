# SPDX-License-Identifier: GPL-3.0-or-later
# shellcheck shell=sh
#
# Board 32's prompt: the directory in blue and a dim $, after user@host in green over SSH.
# Only Fedora's default PS1 is replaced, and bash-color-prompt.sh, sourced later, keeps ours.

if [ -n "${BASH_VERSION-}" ] && [ -z "${apex_prompt_disable-}" ] && [ -z "${NO_COLOR-}" ]; then
    case $- in
        *i*)
            if [ "$PS1" = "[\u@\h \W]\\$ " ] || [ "$PS1" = "\\s-\\v\\\$ " ]; then
                if [ -n "${SSH_CONNECTION-}" ]; then
                    PS1='\[\e[32m\]\u@\h\[\e[0;2m\]:\[\e[0;34m\]\w\[\e[0;2m\]\$\[\e[0m\] '
                else
                    PS1='\[\e[34m\]\w\[\e[0;2m\] \$\[\e[0m\] '
                fi
            fi
            ;;
    esac
fi
