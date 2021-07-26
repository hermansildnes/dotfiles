# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

neofetch


# Useful aliases
alias ls='exa'
alias grep='grep --color=auto'

alias qtest='python -m py_compile /home/error/.config/qtile/config.py'
alias qconf='code ~/.config/qtile'
alias qlog='cat ~/.local/share/qtile/qtile.log'
alias config='/usr/bin/git --git-dir=$HOME/dotfiles --work-tree=$HOME'

alias cp='cp -i'
alias ..='cd ..'

# Useful exports
export CLICOLOR=1
export HISTCONTROL=ignoreboth
export TERM=xterm-256color
