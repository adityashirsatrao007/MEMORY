"""
Global API Keys Loader
Usage in any Python project:
    import sys; sys.path.insert(0, '/home/aditya/.config/global-apikeys')
    from load_keys import keys, get

Or one-liner:
    exec(open('/home/aditya/.config/global-apikeys/load_keys.py').read())
"""
import os
from pathlib import Path

_KEYS_FILE = Path('/home/aditya/.config/global-apikeys/keys.env')

def load_keys(override_env=True):
    """Load all API keys from global database into os.environ"""
    loaded = {}
    if not _KEYS_FILE.exists():
        print(f"[global-keys] WARNING: {_KEYS_FILE} not found")
        return loaded
    with open(_KEYS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, val = line.partition('=')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val and (override_env or key not in os.environ):
                os.environ[key] = val
                loaded[key] = val
    return loaded

def get(key, default=None):
    """Get a specific API key by name"""
    load_keys()
    return os.environ.get(key, default)

# Auto-load on import
keys = load_keys()

if __name__ == '__main__':
    print(f"Loaded {len(keys)} API keys:")
    for k, v in sorted(keys.items()):
        masked = v[:8] + '...' + v[-4:] if len(v) > 12 else '***'
        print(f"  {k:<35} = {masked}")
