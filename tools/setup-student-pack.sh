#!/usr/bin/env bash
# MEMORY — Setup GitHub Student Pack integrations
set -euo pipefail

MEMORY_ROOT="${MEMORY_ROOT:-$HOME/Desktop/Projects/MEMORY}"
KEYS_FILE="$HOME/.config/global-apikeys/keys.env"

echo "╔══════════════════════════════════════════════╗"
echo "║   GitHub Student Pack Integration Setup      ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Check if keys.env exists
if [ ! -f "$KEYS_FILE" ]; then
    echo "Creating keys.env..."
    mkdir -p "$(dirname "$KEYS_FILE")"
    touch "$KEYS_FILE"
fi

echo "=== Available Integrations ==="
echo ""
echo "1. GitHub Copilot    — Already configured via .github/copilot-instructions.md"
echo "2. GitHub Codespaces — .devcontainer/devcontainer.json created"
echo "3. DigitalOcean      — \$200 credit (expires 2026-07-31)"
echo "4. MongoDB Atlas     — \$50 credit + free cert"
echo "5. Clerk Auth        — Free Pro plan"
echo "6. Stripe Payments   — No fees on first \$1000"
echo "7. Datadog           — Free 2 years monitoring"
echo "8. Heroku            — \$13/month for 24 months"
echo "9. JetBrains IDEs    — Free while student"
echo "10. FrontendMasters  — 6 months free courses"
echo ""

# DigitalOcean
echo "=== DigitalOcean ($200 credit) ==="
echo "Claim at: https://www.digitalocean.com/education/"
echo "Save your API key:"
read -p "  DigitalOcean API key (or press Enter to skip): " DO_KEY
if [ -n "$DO_KEY" ]; then
    echo "DIGITALOCEAN_API_KEY=$DO_KEY" >> "$KEYS_FILE"
    echo "  ✓ Saved to $KEYS_FILE"
fi

# MongoDB
echo ""
echo "=== MongoDB Atlas ($50 credit) ==="
echo "Claim at: https://cloud.mongodb.com → Free M0 cluster"
echo "Save your connection string:"
read -p "  MongoDB URI (or press Enter to skip): " MONGO_URI
if [ -n "$MONGO_URI" ]; then
    echo "MONGODB_URI=$MONGO_URI" >> "$KEYS_FILE"
    echo "  ✓ Saved to $KEYS_FILE"
fi

# Clerk
echo ""
echo "=== Clerk Auth (Free Pro) ==="
echo "Claim at: https://clerk.com/education"
read -p "  Clerk Publishable Key (or press Enter to skip): " CLERK_PK
if [ -n "$CLERK_PK" ]; then
    read -p "  Clerk Secret Key: " CLERK_SK
    echo "CLERK_PUBLISHABLE_KEY=$CLERK_PK" >> "$KEYS_FILE"
    echo "CLERK_SECRET_KEY=$CLERK_SK" >> "$KEYS_FILE"
    echo "  ✓ Saved to $KEYS_FILE"
fi

# Stripe
echo ""
echo "=== Stripe (No fees on first \$1000) ==="
echo "Claim at: https://stripe.com/education"
read -p "  Stripe Secret Key (or press Enter to skip): " STRIPE_SK
if [ -n "$STRIPE_SK" ]; then
    read -p "  Stripe Publishable Key: " STRIPE_PK
    echo "STRIPE_SECRET_KEY=$STRIPE_SK" >> "$KEYS_FILE"
    echo "STRIPE_PUBLISHABLE_KEY=$STRIPE_PK" >> "$KEYS_FILE"
    echo "  ✓ Saved to $KEYS_FILE"
fi

# Datadog
echo ""
echo "=== Datadog (Free 2 years) ==="
echo "Claim at: https://www.datadoghq.com/student/"
read -p "  Datadog API Key (or press Enter to skip): " DD_KEY
if [ -n "$DD_KEY" ]; then
    echo "DD_API_KEY=$DD_KEY" >> "$KEYS_FILE"
    echo "  ✓ Saved to $KEYS_FILE"
fi

# Heroku
echo ""
echo "=== Heroku (\$13/month for 24 months) ==="
echo "Claim at: https://www.heroku.com/github-student"
read -p "  Heroku API Key (or press Enter to skip): " HEROKU_KEY
if [ -n "$HEROKU_KEY" ]; then
    echo "HEROKU_API_KEY=$HEROKU_KEY" >> "$KEYS_FILE"
    echo "  ✓ Saved to $KEYS_FILE"
fi

echo ""
echo "=== Setup Complete ==="
echo "Keys saved to: $KEYS_FILE"
echo ""
echo "To use DigitalOcean for MEMORY dashboard:"
echo "  doctl compute droplet create memory-api --image ubuntu-22-04 --size s-1vcpu-1gb"
echo ""
echo "To use MongoDB as vector DB:"
echo "  Run: make seed-mongo"
echo ""
echo "To start all services:"
echo "  bash tools/start-infra.sh"
