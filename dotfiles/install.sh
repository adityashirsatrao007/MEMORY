#!/bin/bash
# Copyright (c) 2026 Aditya Shirsatrao. All rights reserved.
# Proprietary — see LICENSE file. No copying, cloning, or distribution.
# Dotfiles install script — symlinks configs to their proper locations
# Usage: ./install.sh

set -e
DOTFILES_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "📂 Installing dotfiles from: $DOTFILES_DIR"

# Bash
ln -sf "$DOTFILES_DIR/bash/bashrc" "$HOME/.bashrc"
echo "  ✅ .bashrc"

# Starship
mkdir -p "$HOME/.config"
ln -sf "$DOTFILES_DIR/starship/starship.toml" "$HOME/.config/starship.toml"
echo "  ✅ starship.toml"

# Tmux
ln -sf "$DOTFILES_DIR/tmux/tmux.conf" "$HOME/.tmux.conf"
echo "  ✅ .tmux.conf"

# Git
ln -sf "$DOTFILES_DIR/git/gitconfig" "$HOME/.gitconfig"
echo "  ✅ .gitconfig"

echo ""
echo "✅ All dotfiles symlinked. Source your shell:"
echo "   source ~/.bashrc"
