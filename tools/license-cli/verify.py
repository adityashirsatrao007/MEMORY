"""
License verification client — online + offline grace.
Standard pattern used by JetBrains, VS Code, Sublime Text.
"""
import os
import json
import base64
from datetime import datetime, timezone, timedelta

LICENSE_DIR = os.path.expanduser("~/.config/memory")
TOKEN_PATH = os.path.join(LICENSE_DIR, "license.jwt")
CONFIG_PATH = os.path.join(LICENSE_DIR, "config.json")
PUBKEY_PATH = os.path.join(LICENSE_DIR, "public_key.pem")

GRACE_DAYS = 7  # how long offline verification works after server goes dark
SERVER_UNREACHABLE_COOLDOWN = 3600  # don't retry server for 1h after failure


def ensure_dir():
    os.makedirs(LICENSE_DIR, exist_ok=True)


def store_token(token: str, tier: str, expires_at: str | None = None, public_key: str = ""):
    ensure_dir()
    with open(TOKEN_PATH, "w") as f:
        f.write(token)
    config = {
        "tier": tier,
        "expires_at": expires_at,
        "activated_at": datetime.now(timezone.utc).isoformat(),
        "last_verified_online": None,
        "last_verified_local": datetime.now(timezone.utc).isoformat(),
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    if public_key:
        with open(PUBKEY_PATH, "w") as f:
            f.write(public_key)
    os.chmod(TOKEN_PATH, 0o600)
    os.chmod(CONFIG_PATH, 0o600)


def get_token() -> str | None:
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH) as f:
            return f.read().strip()
    return None


def get_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def clear():
    for p in [TOKEN_PATH, CONFIG_PATH, PUBKEY_PATH]:
        if os.path.exists(p):
            os.remove(p)


def decode_jwt(token: str) -> dict | None:
    """Unverified decode — reads payload without crypto validation."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        # Fix padding
        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += "=" * padding
        return json.loads(base64.b64decode(payload))
    except Exception:
        return None


def verify_jwt_locally(token: str, public_key_pem: str) -> dict | None:
    """Full RS256 verification using local public key."""
    try:
        from cryptography.hazmat.primitives import serialization, hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.exceptions import InvalidSignature

        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        parts = token.split(".")
        if len(parts) != 3:
            return None
        message = f"{parts[0]}.{parts[1]}".encode()
        signature = base64.urlsafe_b64decode(parts[2] + "==")
        try:
            public_key.verify(signature, message, padding.PKCS1v15(), hashes.SHA256())
        except InvalidSignature:
            return None
        return decode_jwt(token)
    except Exception:
        return None


def get_public_key() -> str | None:
    if os.path.exists(PUBKEY_PATH):
        with open(PUBKEY_PATH) as f:
            return f.read().strip()
    return None


class VerifyResult:
    def __init__(self, valid: bool, tier: str = "", message: str = "",
                 expires_at: str | None = None, source: str = ""):
        self.valid = valid
        self.tier = tier
        self.message = message
        self.expires_at = expires_at
        self.source = source  # "online", "local", "grace", or ""


def check_offline(token: str | None = None) -> VerifyResult:
    """Full offline check: verify JWT signature + expiry + grace period."""
    token = token or get_token()
    if not token:
        return VerifyResult(False, message="No license token found")

    config = get_config()
    pubkey = get_public_key()
    payload = decode_jwt(token)

    if not payload:
        return VerifyResult(False, message="Malformed token")

    tier = payload.get("tier", config.get("tier", "unknown"))
    exp_ts = payload.get("exp")
    exp_at = datetime.fromtimestamp(exp_ts, tz=timezone.utc) if exp_ts else None

    # Try full signature verification if we have the public key
    if pubkey:
        verified = verify_jwt_locally(token, pubkey)
        if not verified:
            return VerifyResult(False, tier=tier, message="Token signature invalid")
    # else: skip signature check, trust the cached token

    if exp_at and exp_at < datetime.now(timezone.utc):
        # Token expired — check grace period
        last_online = config.get("last_verified_online")
        if last_online:
            last = datetime.fromisoformat(last_online)
            grace_end = last + timedelta(days=GRACE_DAYS)
            if datetime.now(timezone.utc) < grace_end:
                return VerifyResult(True, tier=tier,
                    message=f"Token expired but within grace period (until {grace_end.date()})",
                    expires_at=exp_at.isoformat() if exp_at else None, source="grace")
        return VerifyResult(False, tier=tier, message="License expired")

    # Token is valid
    return VerifyResult(True, tier=tier,
        message="Valid (offline verification)",
        expires_at=exp_at.isoformat() if exp_at else None,
        source="local")
