"""
JWT verification client — validates license tokens locally.
"""
import os
import sys
import json
from datetime import datetime, timezone

LICENSE_DIR = os.path.expanduser("~/.config/memory")
TOKEN_PATH = os.path.join(LICENSE_DIR, "license.jwt")
CONFIG_PATH = os.path.join(LICENSE_DIR, "config.json")

PUBLIC_KEY_PATH = os.path.join(LICENSE_DIR, "public_key.pem")
DEFAULT_PUBLIC_KEY = os.path.join(
    os.path.dirname(__file__), "..", "license-server", "public_key.pem"
)


def ensure_dir():
    os.makedirs(LICENSE_DIR, exist_ok=True)


def store_token(token: str, tier: str, expires_at: str | None = None):
    ensure_dir()
    with open(TOKEN_PATH, "w") as f:
        f.write(token)
    config = {"tier": tier, "expires_at": expires_at, "activated_at": datetime.now(timezone.utc).isoformat()}
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
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


def clear():
    for p in [TOKEN_PATH, CONFIG_PATH]:
        if os.path.exists(p):
            os.remove(p)


def verify_locally(token: str) -> dict | None:
    """Unverified decode — inspect payload without verifying signature.
    Full verification requires the server /verify endpoint with the public key.
    """
    try:
        import base64
        parts = token.split(".")
        if len(parts) != 3:
            return None
        padding = 4 - len(parts[1]) % 4
        if padding != 4:
            parts[1] += "=" * padding
        payload = json.loads(base64.b64decode(parts[1]))
        return payload
    except Exception:
        return None
