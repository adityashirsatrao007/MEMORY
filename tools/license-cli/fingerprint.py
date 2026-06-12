"""
Machine fingerprinting — cross-platform unique machine ID.
"""
import os
import sys
import json
import socket
import hashlib
import subprocess


def get_fingerprint_data() -> dict:
    data = {
        "hostname": socket.gethostname(),
        "platform": sys.platform,
    }
    if sys.platform == "linux":
        for path in ["/etc/machine-id", "/var/lib/dbus/machine-id"]:
            if os.path.exists(path):
                with open(path) as f:
                    data["machine_id"] = f.read().strip()
                    break
        try:
            r = subprocess.run(
                ["cat", "/proc/cpuinfo"], capture_output=True, text=True, timeout=5
            )
            for line in r.stdout.split("\n"):
                if "Serial" in line:
                    data["cpu_serial"] = line.split(":")[-1].strip()
                    break
        except Exception:
            pass
    elif sys.platform == "darwin":
        try:
            r = subprocess.run(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                capture_output=True, text=True, timeout=5,
            )
            for line in r.stdout.split("\n"):
                if "IOPlatformUUID" in line:
                    data["uuid"] = line.split('"')[-2]
                    break
        except Exception:
            pass
    elif sys.platform == "win32":
        try:
            r = subprocess.run(
                ["wmic", "csproduct", "get", "UUID"],
                capture_output=True, text=True, timeout=5,
            )
            lines = r.stdout.strip().split("\n")
            if len(lines) > 1:
                data["uuid"] = lines[1].strip()
        except Exception:
            pass
    return data


def fingerprint() -> str:
    data = get_fingerprint_data()
    raw = json.dumps(data, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def pretty_print() -> str:
    data = get_fingerprint_data()
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    print(fingerprint())
