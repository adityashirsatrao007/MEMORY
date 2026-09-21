#!/usr/bin/env bash
# Usage: add_key.sh KEY_NAME "key_value"
# Adds a new API key to the global database
if [[ -z "$1" || -z "$2" ]]; then
    echo "Usage: $0 KEY_NAME key_value"
    exit 1
fi
KEYS_FILE="$HOME/.config/global-apikeys/keys.env"
KEY="$1"
VAL="$2"
# Remove existing entry if any
sed -i "/^${KEY}=/d" "$KEYS_FILE"
# Append new entry
echo "${KEY}=\"${VAL}\"" >> "$KEYS_FILE"
echo "✅ Added/updated: $KEY"
