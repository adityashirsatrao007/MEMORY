# Security — Password Hashing, Repository Hygiene, Guardrails

> Extracted from `GEMINI.md`. See `memory/modules/02-cli-tools.md` for secret scanning tools (gitleaks, trufflehog, trivy), `memory/modules/01-core-rules.md` for production security standards.

---

## 🛡️ Repository Hygiene & Security Guardrails (Zero-Vulnerability Codebase)

The agent MUST enforce strict repository hygiene and security guardrails to ensure no secrets, internal assets, or architectural flaws are exposed.

### 1. Repository Hygiene & Git Cleanliness
- **Zero Secrets committed:** NEVER commit `.env`, `.env.local`, or any credentials/keys. Use `.env.example`.
- **Strict `.gitignore` enforcement:** Ensure `node_modules/`, build output, and system files are ignored.
- **No raw design assets:** Keep `.psd`, Sketch, or Illustrator files out of repo.
- **No operational leaks:** Keep production deployment files separated from source directories.
- **Pre-flight Commit check:** Always run `git status` to verify no build artifacts or config overrides are staged.

### 2. Authentication & Authorization Security
- **Secure Cookie Configuration:** Session cookies/JWT tokens MUST carry:
  - `HttpOnly` (prevents XSS access to tokens)
  - `Secure` (only sent over HTTPS)
  - `SameSite=Lax` or `SameSite=Strict` (prevents CSRF)
- **Secure Auth Responses:** NEVER return password hashes, internal roles, salt, or DB metadata. Project safe fields only.
- **Safe Error Handling:** Never return raw stack traces, DB query logs, or server internals. Log securely to stdout/files.

### 3. API Security & Infrastructure Protection
- **Input Validation & Rate Limiting:** All endpoints must enforce input validation (Pydantic, Zod, Joi) and rate limiting (token bucket pattern).
- **Zero Default Credentials:** Never document default admin credentials. Use dynamic init scripts.
- **Conceal Architecture details:** Avoid exposing `nginx.conf`, `docker-compose.yml` with default ports.
- **Automated Scanning Guardrails:** Run `semgrep`, `gitleaks`, and `trivy` in pre-commit hooks and CI.
- **"Clean Commit" Workflow:** Run `git diff | delta` before pushing. No "Push First, Fix Later."

### 4. Automated Scanning Tools
| Tool | When | What it finds |
|------|------|---------------|
| `gitleaks` | Pre-commit / CI | Secrets in git history |
| `trufflehog` | Pre-commit / audit | Verified leaked credentials |
| `trivy` | CI / pre-deploy | CVEs, IaC misconfigurations, SBOM issues |
| `semgrep` | Pre-commit / CI | Logic bugs, security patterns, SAST |

---

## 🔐 Password Security — Hashing, Salting, Bcrypt & Argon2

### Core Concepts

**Password Hashing** is a one-way cryptographic transformation. Plain hashes alone are never enough for password storage.

**Why unsalted hashes fail:**
- Hash tables: pre-computed databases mapping passwords → hashes (instant lookup)
- Rainbow tables: compressed version (space-time tradeoff)
- Dictionary attacks: pre-computed wordlists + common patterns
- Modern GPUs compute billions of hashes/second

**Salting** adds a cryptographically random value per credential:
```
hash(password + salt) → stored_hash
```

### Salting Rules (OWASP-Compliant)
- ✅ Generate a **new unique salt per credential**
- ✅ Use a **CSPRNG** (Cryptographically Secure Pseudo-Random Number Generator)
- ✅ Salt size: **32-64 bytes** minimum
- ✅ Store: `username | salt (cleartext) | hash` together
- ✅ Re-salt on every password reset
- ❌ Never use system-wide salts
- ❌ Never reveal if two users share a password

### Algorithm Comparison

| Algorithm | Memory Hard | GPU Resistant | OWASP Rec. | Use Case |
|-----------|-------------|----------------|------------|----------|
| **MD5** | ❌ | ❌ | ❌ NEVER | Legacy only |
| **SHA-256** | ❌ | ❌ | ❌ NEVER | Data integrity |
| **bcrypt** | ✅ (moderate) | ✅ | ✅ Yes | Most production apps |
| **scrypt** | ✅ (high RAM) | ✅ | ✅ Yes | High-security |
| **Argon2id** | ✅ (best) | ✅ | ✅ **Top Pick** | Modern systems |
| **PBKDF2** | ❌ | Partial | ✅ (FIPS) | FIPS compliance |

### Argon2 Deep Dive
**Argon2id** = hybrid of Argon2d + Argon2i
- **Parameters:** `time` (iterations), `memory` (RAM in KB), `parallelism` (threads)
- **Winner of Password Hashing Competition (2015)**
- Recommended minimum params: `time=2, memory=65536 (64MB), parallelism=2`

### bcrypt Deep Dive
- **Cost factor** is adjustable — scales with hardware
- Embeds salt within output hash string (`$2b$12$...`)
- Max password length: **72 bytes** (silently truncates longer!)
- Recommended cost: **12+** (~100-300ms on your server)

### Production Code Patterns

**Node.js — bcrypt:**
```js
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;
const hash = await bcrypt.hash(password, SALT_ROUNDS);
const match = await bcrypt.compare(candidatePassword, storedHash);
```

**Node.js — Argon2:**
```js
const argon2 = require('argon2');
const hash = await argon2.hash(password, {
  type: argon2.argon2id,
  memoryCost: 65536,
  timeCost: 2,
  parallelism: 2,
});
const match = await argon2.verify(storedHash, candidatePassword);
```

**Python — bcrypt:**
```python
import bcrypt
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
match = bcrypt.checkpw(candidate.encode(), hash)
```

**Python — Argon2:**
```python
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=2)
hash = ph.hash(password)
ph.verify(hash, candidate)  # raises VerifyMismatchError if wrong
```

### Decision Tree: Which to Use
```
New project (2025)?        → Use Argon2id (best security, PHC winner)
Legacy Node.js/PHP stack?  → Use bcrypt (battle-tested)
FIPS compliance needed?    → Use PBKDF2-SHA256
High-security + RAM?       → Use scrypt
```

### Breach Response Protocol
1. **Immediately** treat all passwords as compromised
2. Notify users — force password reset
3. Generate new salts during reset
4. Increase bcrypt cost / Argon2 memory if possible
5. Enable MFA for all accounts

### Reference Sources
- Auth0: [Adding Salt to Hashing](https://auth0.com/blog/adding-salt-to-hashing-a-better-way-to-store-passwords/)
- Proton: [Password Hashing and Salting](https://proton.me/blog/password-hashing-salting)
- Stytch: [Argon2 vs bcrypt vs scrypt](https://stytch.com/blog/argon2-vs-bcrypt-vs-scrypt/)
