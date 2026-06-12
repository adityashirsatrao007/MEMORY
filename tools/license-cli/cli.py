#!/usr/bin/env python3
"""
MEMORY License CLI — activate, verify, and manage license tokens.

Usage:
  memory activate                # Interactive activation
  memory activate <KEY>          # Activate with key
  memory verify                  # Check license status
  memory status                  # Same as verify
  memory clear                   # Remove local license data
  memory fingerprint             # Show machine fingerprint
"""
import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import URLError

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fingerprint import fingerprint, pretty_print as fp_pretty
from verify import store_token, get_token, get_config, clear, verify_locally

API_URL = os.getenv("MEMORY_LICENSE_API", "http://localhost:8443")


def api_post(path: str, data: dict) -> dict:
    url = f"{API_URL}{path}"
    body = json.dumps(data).encode()
    req = Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urlopen(req, timeout=15) as resp:
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
    import socket
    import sys as _sys
    data = {
        "license_key": key,
        "machine_fingerprint": fp,
        "hostname": socket.gethostname(),
        "platform": _sys.platform,
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

    fp = fingerprint()
    try:
        resp = api_post("/verify", {"token": token, "machine_fingerprint": fp})
    except RuntimeError as e:
        print(f"Verification failed: {e}")
        # Try local decode as fallback
        payload = verify_locally(token)
        if payload:
            print(f"Local token info: tier={payload.get('tier')}, license={payload.get('license_key')}")
        sys.exit(1)

    if resp.get("valid"):
        config = get_config()
        print(f"License: VALID")
        print(f"Tier: {resp.get('tier', config.get('tier', 'unknown'))}")
        if config.get("expires_at"):
            print(f"Expires: {config['expires_at']}")
        else:
            print("Expires: never")
    else:
        print(f"License: INVALID — {resp.get('message', 'Unknown error')}")
        sys.exit(1)


def cmd_status(args):
    config = get_config()
    token = get_token()
    if not token:
        print("No license activated.")
        sys.exit(0)
    payload = verify_locally(token)
    if payload:
        print(f"License Key: {payload.get('license_key', 'N/A')}")
        print(f"Tier: {payload.get('tier', config.get('tier', 'N/A'))}")
        print(f"Email: {payload.get('email', 'N/A')}")
        if payload.get("exp"):
            from datetime import datetime
            exp = datetime.fromtimestamp(payload["exp"])
            print(f"Expires: {exp.isoformat()}")
            if exp < datetime.now():
                print("Status: EXPIRED")
            else:
                print("Status: Active")
        else:
            print("Expires: never")
            print("Status: Active")
        print(f"Token: {token[:40]}...")
    else:
        print("Token present but malformed. Run 'memory activate' again.")


def cmd_clear(args):
    clear()
    print("License data cleared.")


def cmd_fingerprint(args):
    print(fp_pretty())
    print(f"SHA-256: {fingerprint()}")


def main():
    parser = argparse.ArgumentParser(description="MEMORY License CLI")
    sub = parser.add_subparsers(dest="command")

    p_activate = sub.add_parser("activate", help="Activate a license key")
    p_activate.add_argument("key", nargs="?", help="License key (omit for prompt)")

    sub.add_parser("verify", help="Verify license with server")
    sub.add_parser("status", help="Show local license status")
    sub.add_parser("clear", help="Remove local license data")
    sub.add_parser("fingerprint", help="Show machine fingerprint")

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
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
