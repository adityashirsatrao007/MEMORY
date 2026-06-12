# License System — Security Recommendations

## Threat Model

| Threat | Impact | Mitigation |
|--------|--------|------------|
| Token theft | Unauthorized use | Machine binding + short expiry + HTTPS |
| Key guessability | Free licenses | 12-char hex random (2^48 space) |
| JWT forgery | Spoofed tokens | RS256 with 4096-bit key |
| Token replay | Multiple machines | Machine fingerprint binding |
| Reverse engineering | Bypass checks | Obfuscate verification; server-enforced |
| Revoked-key reuse | Stolen keys | Server-side revocation + online verification |

## Server Security

1. **Run behind reverse proxy**: nginx/Caddy with HTTPS (Let's Encrypt)
2. **Rate limit endpoints**: 5 attempts/min per IP on `/activate`
3. **Database encryption**: Encrypt `tokens` column at rest
4. **Admin panel**: IP whitelist + strong admin token (32+ chars)
5. **Key rotation**: Rotate RS256 key pair every 90 days

## Client Security

1. **Token storage**: `~/.config/memory/license.jwt` with `chmod 600`
2. **Machine binding**: SHA-256 of hardware identifiers prevents token sharing
3. **Offline grace**: Cache verification for 24h if server unreachable
4. **Tamper detection**: Verify JWT signature locally if server is down

## Offline Grace (Server Down)

The client handles server outages gracefully:

1. **Server reachable** → online RS256 verify → cache result + extend grace
2. **Server down** → fall back to local JWT signature verify (RS256 via cached public key)
3. **Token expired but within 7-day grace period** → allow with warning
4. **Beyond grace** → block, prompt to visit website

This is the standard pattern used by JetBrains, VS Code, and Sublime Text.

```
Startup:
  ├─ Online verify OK? ──→ RUN (cache last_verified)
  ├─ Server down, token valid? ──→ RUN (offline)
  ├─ Server down, token expired, <7d grace? ──→ RUN with ⚠️
  └─ Beyond grace? ──→ BLOCK
```

## Deployment Checklist

- [ ] Generate unique RS256 key pair per deployment
- [ ] Set `LICENSE_ADMIN_TOKEN` to a 32+ char random string
- [ ] Configure firewall: only expose ports 443 (HTTPS), 8443 (API internal)
- [ ] Enable PostgreSQL SSL (`sslmode=require`)
- [ ] Set up daily database backups
- [ ] Monitor `/activate` for anomalous patterns
- [ ] Revoke leaked keys immediately via admin panel

## Key Formats

```
Trial:      MEM-TRIAL-XXXX-XXXX-XXXX    (3-day expiry, 1 machine)
Pro:        MEM-PRO-XXXX-XXXX-XXXX      (no expiry, 3 machines)
Enterprise: MEM-ENT-XXXX-XXXX-XXXX      (no expiry, unlimited machines)
```

## JWT Payload Structure

```json
{
  "license_key": "MEM-PRO-ABCD-EFGH-IJKL",
  "tier": "pro",
  "email": "user@example.com",
  "machine_fp": "sha256-of-hardware-id",
  "iss": "memory-license-server",
  "iat": 1718000000,
  "exp": 1749536000
}
```
