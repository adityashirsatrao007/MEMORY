#!/usr/bin/env bash
# Global API Keys Loader
# Usage: source ~/.config/global-apikeys/load_keys.sh
KEYS_FILE="$HOME/.config/global-apikeys/keys.env"
if [[ -f "$KEYS_FILE" ]]; then
    set -a
    source "$KEYS_FILE"
    set +a
fi
