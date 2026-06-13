# Copyright (c) 2026 Aditya Shirsatrao. All rights reserved.
# Proprietary — see LICENSE file. No copying, cloning, or distribution.
# rtk auto-pipe — compress long CLI output automatically
# Source this in bashrc to auto-pipe known verbose commands through rtk

__rtk_pipe() {
  local cmd="$*"
  local out
  out=$("$@" 2>&1) || { echo "$out"; return 1; }
  # If output > 5 lines, compress through rtk
  local lines
  lines=$(echo "$out" | wc -l)
  if [ "$lines" -gt 5 ]; then
    echo "$out" | rtk 2>/dev/null || echo "$out"
  else
    echo "$out"
  fi
}

# Auto-pipe wrappers — only for commands known to produce long output
git-diff() { command git diff "$@" | delta; }
git-log() { command git log --oneline -20 "$@"; }
git-status() { command git status --short "$@"; }
eza-tree() { command eza --tree --level 2 --git-ignore "$@"; }
# For arbitrary long output: cmd | rtk
