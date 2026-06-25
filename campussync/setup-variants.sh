#!/bin/bash
set -e

# Base directory
BASE_DIR="/home/aditya/Desktop/Projects/MEMORY"
SRC_DIR="$BASE_DIR/campussync"

# Variants and their ports
variants=("glass" "aurora" "neumorph" "brutalist" "clay")
ports=(3003 3004 3005 3006 3007)

for i in "${!variants[@]}"; do
  var="${variants[$i]}"
  port="${ports[$i]}"
  target_dir="$BASE_DIR/campussync-$var"
  
  echo "Creating variant: $var on port $port..."
  mkdir -p "$target_dir"
  
  # Copy project files
  cp "$SRC_DIR/package.json" "$target_dir/"
  cp "$SRC_DIR/index.html" "$target_dir/"
  cp "$SRC_DIR/eslint.config.js" "$target_dir/"
  
  # Copy src directory
  cp -r "$SRC_DIR/src" "$target_dir/"
  
  # Symlink node_modules
  ln -sf "$SRC_DIR/node_modules" "$target_dir/node_modules"
  
  # Write custom vite.config.js for this variant
  cat << EOF > "$target_dir/vite.config.js"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    port: $port,
  }
})
EOF

done

echo "All variants created and linked!"
