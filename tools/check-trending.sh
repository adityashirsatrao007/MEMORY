#!/usr/bin/env bash
# Daily GitHub trending scan for agent self-improvement.
# Usage: tools/check-trending.sh            # run & log once/day (idempotent)
#        tools/check-trending.sh --force    # rerun even if run today
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="$ROOT/memory/memory-bank/trending-log.md"
TODAY="$(date +%Y-%m-%d)"

if [ "${1:-}" != "--force" ] && grep -q "^## $TODAY" "$LOG" 2>/dev/null; then
  echo "already scanned today ($TODAY). Pass --force to rerun."
  exit 0
fi

now="$(date +%Y-%m-%dT%H:%M)"
cat >> "$LOG" <<EOF
## $TODAY  (scanned $now)
EOF
Q="created:%3E$(date -d '-14 days' +%Y-%m-%d)"
gh api "search/repositories?q=$Q&sort=stars&per_page=10" --jq '.items[:10] | .[] | "- \(.full_name) ★\(.stargazers_count) — \(.description // "no desc")"' >> "$LOG" 2>/dev/null || echo "- (trending scan failed)" >> "$LOG"

echo "logged trending scan to $LOG"