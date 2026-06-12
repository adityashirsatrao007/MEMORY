# Audit Trail & Compliance

Premium module — requires Enterprise license.

## Features
- Immutable append-only change log (SHA-256 chained hashes)
- SOC2-ready CSV/JSON export
- Per-user action history with before/after diffs
- Tamper detection: hash chain verification

## Setup
```bash
memory premium install audit-trail
```

Export audit log:
```bash
memory audit export --format csv --since "2026-01-01"
```
