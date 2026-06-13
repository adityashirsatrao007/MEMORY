"""
License enforcement — gated before every meaningful MEMORY operation.
Checks local license, falls back to online verification, then offline grace.
"""
import os
import sys
import json
import base64
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError

LICENSE_DIR = os.path.expanduser("~/.config/memory")
TOKEN_PATH = os.path.join(LICENSE_DIR, "license.jwt")
CONFIG_PATH = os.path.join(LICENSE_DIR, "config.json")
PUBKEY_PATH = os.path.join(LICENSE_DIR, "public_key.pem")
API_URL = os.getenv("MEMORY_LICENSE_API", "https://memory-license-server.onrender.com")
GRACE_DAYS = 7


def require_license():
    """Exit with error if no valid license. Called at the top of every tool.
    Set MEMORY_NON_COMMERCIAL=1 for personal/non-commercial use (skips check)."""
    if os.environ.get("MEMORY_NON_COMMERCIAL") == "1":
        return {"valid": True, "tier": "non-commercial", "source": "env"}
    token = _get_token()
    if not token:
        _die("No license found. Run: memory license activate <KEY>")
    result = _verify(token)
    if not result["valid"]:
        _die(f"License invalid: {result['message']}")
    return result


def _get_token():
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH) as f:
            return f.read().strip()
    return None


def _decode_jwt(token):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += "=" * padding
        return json.loads(base64.b64decode(payload))
    except Exception:
        return None


def _verify(token):
    # Try online first
    try:
        fp = _fingerprint()
        body = json.dumps({"token": token, "machine_fingerprint": fp}).encode()
        req = Request(f"{API_URL}/verify", data=body, method="POST")
        req.add_header("Content-Type", "application/json")
        with urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            if data.get("valid"):
                return {"valid": True, "tier": data.get("tier"), "source": "online"}
            return {"valid": False, "message": data.get("message", "Server rejected")}
    except URLError:
        pass

    # Offline grace
    payload = _decode_jwt(token)
    if not payload:
        return {"valid": False, "message": "Malformed token"}

    exp = payload.get("exp")
    if exp:
        exp_dt = datetime.fromtimestamp(exp, tz=timezone.utc)
        if exp_dt < datetime.now(timezone.utc):
            return {"valid": False, "message": "License expired"}

    if not exp:
        return {"valid": True, "tier": payload.get("tier", "pro"), "source": "offline"}

    return {"valid": True, "tier": payload.get("tier", "unknown"), "source": "offline"}


def _fingerprint():
    import hashlib, platform
    raw = f"{platform.node()}-{platform.system()}-{platform.machine()}"
    return hashlib.sha256(raw.encode()).hexdigest()


def _die(msg):
    print(f"LICENSE REQUIRED: {msg}", file=sys.stderr)
    print("Get a trial key: https://adityashirsatrao007.github.io/MEMORY/docs/pricing.html", file=sys.stderr)
    sys.exit(1)
