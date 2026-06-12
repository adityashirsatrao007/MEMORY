# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x | ✅ Active |

## Reporting a Vulnerability

**Do NOT file a public issue.** Email security concerns to the repository owner or open a [private advisory](https://github.com/adityashirsatrao007/MEMORY/security/advisories).

## Security Practices

### Key Management
- API keys loaded exclusively from `~/.config/global-apikeys/keys.env` — never committed
- `.env` files blocked by `.gitignore` across all projects
- AES-256-GCM envelope encryption for stored API keys (Module 08)

### Scanning (Pre-Commit / CI)
| Tool | Scope |
|------|-------|
| `gitleaks` | Secrets in git history |
| `trufflehog` | Verified leaked credentials |
| `trivy` | CVEs, IaC misconfigurations, SBOM |
| `semgrep` | Logic bugs, SAST patterns |

### Authentication Standards
- Cookies: `HttpOnly` + `Secure` + `SameSite=Lax`
- Rate limiting: Token bucket pattern (Redis atomic)
- Input validation: Pydantic / Zod on every endpoint
- Password hashing: Argon2id (OWASP top pick)

### Repository Hygiene
- No `.env`, credentials, or build artifacts in git
- `pre-commit` hooks run gitleaks + semgrep before every commit
- Guardrails at `~/bin/guardrails/` shadow legacy commands

### Breach Response
1. Treat all passwords as compromised immediately
2. Force password reset for all users
3. Generate new salts, increase hash cost if possible
4. Enable MFA across all accounts
5. Rotate all API keys in `keys.env`
