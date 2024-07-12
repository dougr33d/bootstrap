#!/usr/bin/env bash

TWD=$(git rev-parse --show-toplevel)

####
# TMUX setup

echo "Setting up tmux..."
if [ -f ~/.tmux.conf ]; then
    echo "skipping (found existing tmux.conf)"
else
    ln -s $PWD/tmux/tmux.conf ~/.tmux.conf
    echo "done"
fi

####
# BASH setup

echo
echo "Setting up bash..."

BASHRC="$HOME/.bashrc.dreed"

if grep -q "Begin bootstrap" $BASHRC; then
    echo "skipping (found Begin/End bootstrap sections in bashrc)"
else
    echo ""                                    >> $BASHRC
    echo "### Begin bootstrap"                 >> $BASHRC
    BASH_FILES=$(ls $PWD/bash/*)
    for file in ${BASH_FILES[@]}; do
        fn_base=$(basename "$file")
        echo "...linking ${fn_base}"
        echo ". ${file}"                       >> $BASHRC
    done
    echo "export PATH=\$PATH:$TWD/scripts/bin" >> $BASHRC
    echo "### End bootstrap"                   >> $BASHRC
fi

####
# VIM setup

echo
echo "Setting up vim..."

PLUGDIR=$HOME/.vim/autoload/plug.vim

if [ -d $PLUGDIR ]; then
    echo "skipping vim-plug clone (already exists)"
else
    echo "cloning vim-plug"
    curl -fLo $PLUGDIR --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
fi

if [ -f ~/.vimrc ]; then
    echo "skipping vimrc (found existing vimrc)"
else
    echo "symlinking vimrc"
    ln -s $PWD/vim/vimrc ~/.vimrc

    echo "installing plugins"
    vim +PlugInstall +qall
fi

####
# XFCE setup

echo
echo "Setting up xfce..."

if [[ $(uname) =~ Darwin ]]; then
    echo "skipping XFCE setup (Darwin detected)"
else
    XFKBD_XML=~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml
    if [ -L $XFKBD_XML ]; then
        echo "skipping link (${XFKBD_XML} is already a symlink)"
    else
        echo "linking xfce4 keyboard shortcuts"
        if [ -e $XFKBD_XML ]; then
            cp $XFKBD_XML{,.bak}
        fi
        ln -s $PWD/xfce/xfce4-keyboard-shortcuts.xml $XFKBD_XML
    fi
fi

####
# Search for all required tools

TOOLS="code nvim git gh mosh python3.12"

echo
echo "Looking for all required tools ($TOOLS)..."

NOT_FOUND_COUNT=0
for tool in ${TOOLS[@]}; do
    if ! command -v "$tool" >& /dev/null; then
        echo "-> did NOT find $tool"
        NOT_FOUND_COUNT=$(($NOT_FOUND_COUNT+1))
    fi
done
if [[ $NOT_FOUND_COUNT -gt 0 ]]; then
    echo "Missing $NOT_FOUND_COUNT tool(s)"
else
    echo "All required tools found."
fi
