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

if grep -q "Begin bootstrap" ~/.bashrc; then
    echo "skipping (found Begin/End bootstrap sections in bashrc)"
else
    echo "Setting up aliases"
    echo ""                                    >> ~/.bashrc
    echo "### Begin bootstrap"                 >> ~/.bashrc
    echo ". $PWD/bash/vars"                    >> ~/.bashrc
    echo ". $PWD/bash/aliases"                 >> ~/.bashrc
    echo ". $PWD/bash/scripts"                 >> ~/.bashrc
    echo "export PATH=\$PATH:$TWD/scripts/bin" >> ~/.bashrc
    echo "### End bootstrap"                   >> ~/.bashrc
    echo ""                                    >> ~/.bashrc
fi

####
# VIM setup

echo
echo "Setting up vim..."

if [ -d ~/.vim/bundle/Vundle.vim ]; then
    echo "skipping Vundle clone (already exists)"
else
    echo "cloning vundle"
    git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
fi

if [ -f ~/.vimrc ]; then
    echo "skipping vimrc (found existing vimrc)"
else
    echo "symlinking vimrc"
    ln -s $PWD/vim/vimrc ~/.vimrc

    echo "installing plugins"
    vim +PluginInstall +qall
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

