#!/usr/bin/env python3
"""
MEMORY License CLI — activate, verify, and manage license tokens.

Usage:
  memory activate                # Interactive activation
  memory activate <KEY>          # Activate with key
  memory verify                  # Check license status (online + offline fallback)
  memory status                  # Show local license info
  memory clear                   # Remove local license data
  memory fingerprint             # Show machine fingerprint
"""
import os
import sys
import json
import socket
import shutil
import tempfile
import argparse
import tarfile
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fingerprint import fingerprint, pretty_print as fp_pretty
from verify import (
    store_token, get_token, get_config, save_config, clear,
    check_offline, decode_jwt, VerifyResult
)

API_URL = os.getenv("MEMORY_LICENSE_API", "http://localhost:8443")
OFFLINE_OK = True  # allow grace when server is down


def api_post(path: str, data: dict) -> dict:
    url = f"{API_URL}{path}"
    body = json.dumps(data).encode()
    req = Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except URLError as e:
        if hasattr(e, "read"):
            try:
                err = json.loads(e.read())
                raise RuntimeError(err.get("detail", str(e)))
            except Exception:
                raise RuntimeError(str(e))
        raise RuntimeError(str(e))


def cmd_activate(args):
    key = args.key or input("Enter License Key: ").strip()
    if not key:
        print("No license key provided.")
        sys.exit(1)

    fp = fingerprint()
    data = {
        "license_key": key,
        "machine_fingerprint": fp,
        "hostname": socket.gethostname(),
        "platform": sys.platform,
    }

    print(f"Activating {key[:12]}...{key[-4:]}")
    try:
        resp = api_post("/activate", data)
    except RuntimeError as e:
        print(f"Activation failed: {e}")
        sys.exit(1)

    store_token(resp["token"], resp["tier"], resp.get("expires_at"))
    print(f"Activated! Tier: {resp['tier']}")
    if resp.get("expires_at"):
        print(f"Expires: {resp['expires_at']}")
    else:
        print("License: never expires")
    print("Token saved to ~/.config/memory/license.jwt")


def cmd_verify(args):
    token = get_token()
    if not token:
        print("No license token found. Run 'memory activate' first.")
        sys.exit(1)

    # Try online first
    fp = fingerprint()
    online = None
    try:
        resp = api_post("/verify", {"token": token, "machine_fingerprint": fp})
        if resp.get("valid"):
            config = get_config()
            config["last_verified_online"] = datetime.now(timezone.utc).isoformat()
            save_config(config)
            online = resp
    except RuntimeError:
        online = None

    if online:
        config = get_config()
        print(f"License: VALID (online)")
        print(f"Tier: {online.get('tier', config.get('tier', 'unknown'))}")
        if config.get("expires_at"):
            print(f"Expires: {config['expires_at']}")
        else:
            print("Expires: never")
        return

    # Server unreachable — fall back to offline + grace
    print(f"License server unreachable — checking offline...")
    result = check_offline(token)
    if result.valid:
        print(f"License: VALID ({result.source})")
        print(f"Tier: {result.tier}")
        if result.expires_at:
            print(f"Expires: {result.expires_at}")
        else:
            print("Expires: never")
        if result.source == "grace":
            print(f"⚠️  Grace period — server has been unreachable. {result.message}")
        else:
            print("(Offline verification — cached signature valid)")
    else:
        print(f"License: INVALID — {result.message}")
        if "expired" in result.message.lower():
            print("Visit https://github.com/adityashirsatrao007/MEMORY to renew.")
        sys.exit(1)


def cmd_status(args):
    config = get_config()
    token = get_token()
    if not token:
        print("No license activated.")
        return

    payload = decode_jwt(token)
    if not payload:
        print("Token present but malformed. Run 'memory activate' again.")
        return

    result = check_offline(token)
    print(f"License Key: {payload.get('license_key', 'N/A')}")
    print(f"Tier: {payload.get('tier', config.get('tier', 'N/A'))}")
    print(f"Email: {payload.get('email', 'N/A')}")
    if payload.get("exp"):
        exp = datetime.fromtimestamp(payload["exp"])
        print(f"Expires: {exp.isoformat()}")
        print(f"Status: {'Active' if result.valid else 'EXPIRED'}")
    else:
        print("Expires: never")
        print("Status: Active (never expires)")
    last_online = config.get("last_verified_online", "never")
    print(f"Last online check: {last_online}")
    print(f"Token: {token[:40]}...")


def cmd_clear(args):
    clear()
    print("License data cleared.")


def cmd_fingerprint(args):
    print(fp_pretty())
    print(f"SHA-256: {fingerprint()}")


PREMIUM_DIR = Path.home() / ".config" / "memory" / "premium"


def cmd_premium_list(args):
    """List available premium modules from the server."""
    token = get_token()
    if not token:
        print("No license activated. Activate first with 'memory activate'.")
        sys.exit(1)

    fp = fingerprint()
    try:
        resp = api_post("/premium/modules", {"token": token, "machine_fingerprint": fp})
    except RuntimeError as e:
        print(f"Failed to fetch premium modules: {e}")
        sys.exit(1)

    if not resp.get("modules"):
        print("No premium modules available for your tier.")
        return

    print(f"Premium Modules — Tier: {resp.get('tier', 'unknown')}")
    print("=" * 50)
    for mod in resp["modules"]:
        installed = "✓" if (PREMIUM_DIR / mod["slug"]).exists() else " "
        print(f" [{installed}] {mod['name']} v{mod['version']}")
        print(f"     {mod['description']}")
        if installed == " ":
            print(f"     memory premium install {mod['slug']}")
        print()


def cmd_premium_install(args):
    """Download and install a premium module."""
    token = get_token()
    if not token:
        print("No license activated. Activate first with 'memory activate'.")
        sys.exit(1)

    fp = fingerprint()
    try:
        resp = api_post("/premium/modules", {"token": token, "machine_fingerprint": fp})
    except RuntimeError as e:
        print(f"Failed to fetch premium modules: {e}")
        sys.exit(1)

    slug = args.module
    module = next((m for m in resp.get("modules", []) if m["slug"] == slug), None)
    if not module:
        print(f"Module '{slug}' not found or not available for your tier.")
        print("Run 'memory premium list' to see available modules.")
        sys.exit(1)

    print(f"Downloading {module['name']} v{module['version']}...")
    try:
        data = api_post(f"/premium/download/{slug}", {"token": token, "machine_fingerprint": fp})
    except RuntimeError as e:
        print(f"Download failed: {e}")
        sys.exit(1)

    PREMIUM_DIR.mkdir(parents=True, exist_ok=True)
    dest = PREMIUM_DIR / slug
    if dest.exists():
        shutil.rmtree(dest)

    # The server returns the module content as a base64-encoded tarball
    import base64
    tarball = base64.b64decode(data["archive"])
    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as f:
        f.write(tarball)
        f.flush()
        with tarfile.open(f.name, "r:gz") as tar:
            tar.extractall(path=PREMIUM_DIR)
    os.unlink(f.name)

    # Save metadata
    meta = PREMIUM_DIR / slug / ".meta.json"
    with open(meta, "w") as mf:
        json.dump(module, mf, indent=2)

    print(f"Installed to {PREMIUM_DIR / slug}")
    if module.get("docs"):
        print(f"Read more: {module['docs']}")


def cmd_premium_uninstall(args):
    """Remove a premium module."""
    slug = args.module
    dest = PREMIUM_DIR / slug
    if not dest.exists():
        print(f"Module '{slug}' not installed.")
        sys.exit(1)
    shutil.rmtree(dest)
    print(f"Uninstalled {slug}")


def main():
    parser = argparse.ArgumentParser(description="MEMORY License CLI")
    sub = parser.add_subparsers(dest="command")

    p_activate = sub.add_parser("activate", help="Activate a license key")
    p_activate.add_argument("key", nargs="?", help="License key (omit for prompt)")

    sub.add_parser("verify", help="Verify license (online + offline fallback)")
    sub.add_parser("status", help="Show local license status")
    sub.add_parser("clear", help="Remove local license data")
    sub.add_parser("fingerprint", help="Show machine fingerprint")
    p_premium = sub.add_parser("premium", help="Manage premium modules")
    p_premium.add_argument("action", choices=["list", "install", "uninstall"], help="Action")
    p_premium.add_argument("module", nargs="?", help="Module slug (for install/uninstall)")

    args = parser.parse_args()
    if args.command == "activate":
        cmd_activate(args)
    elif args.command == "verify":
        cmd_verify(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "clear":
        cmd_clear(args)
    elif args.command == "fingerprint":
        cmd_fingerprint(args)
    elif args.command == "premium":
        if args.action == "list":
            cmd_premium_list(args)
        elif args.action == "install":
            cmd_premium_install(args)
        elif args.action == "uninstall":
            cmd_premium_uninstall(args)
        else:
            print("Usage: memory premium {list|install|uninstall} [module]")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
