
#
# .bashrc.override.sh
#

parse_git_branch() {
  git branch 2>/dev/null | sed -n '/\* /s///p'
}

# persistent bash history
HISTFILE=~/.bash_history
PROMPT_COMMAND="history -a; $PROMPT_COMMAND"

# set some env vars
source /entrypoint

# Modify prompt to show git branch
export PS1="\[\e[32m\]\u@\h \[\e[34m\]\w \[\e[33m\]\$(parse_git_branch)\[\e[0m\] \$ "

# restore default shell options
set +o errexit
set +o pipefail
set +o nounset

# start ssh-agent
# https://code.visualstudio.com/docs/remote/troubleshooting
eval "$(ssh-agent -s)"
