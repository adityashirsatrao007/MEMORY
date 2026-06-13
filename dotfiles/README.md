# Aditya's Dotfiles

Disaster recovery for my dev environment. One `git clone` + `./install.sh` to restore everything.

## What's Included

| Config | Path | Purpose |
|--------|------|---------|
| `bash/bashrc` | `~/.bashrc` | Shell aliases, env vars, PATH, venv activation |
| `starship/starship.toml` | `~/.config/starship.toml` | Shell prompt with git/node/python context |
| `tmux/tmux.conf` | `~/.tmux.conf` | Terminal multiplexer config |
| `git/gitconfig` | `~/.gitconfig` | Git defaults, aliases, user identity |

## Quick Setup

```bash
git clone https://github.com/adityashirsatrao007/MEMORY.git ~/Desktop/Projects/MEMORY
cd ~/Desktop/Projects/MEMORY/dotfiles
chmod +x install.sh
./install.sh
source ~/.bashrc
```

## Recovery

If machine dies:
1. `git clone` the MEMORY repo
2. Navigate to `dotfiles/` directory and run `./install.sh`
3. All configs restored via symlinks
