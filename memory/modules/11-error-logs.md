# Critical Error Logs & Historical Diagnoses

This module serves as a persistent error ledger for Antigravity. Before executing related systems, check this ledger to avoid repeating known historical failures on this machine.

## 1. Out-of-Memory (OOM) / Hard Freeze from Massive Scripts
**Error:** Running a massive setup script that concurrently triggered `apt-get install chromium-browser` (heavy Snap dependencies), `cargo install` (heavy Rust compilation), and `ollama pull` (3GB+ downloads) resulted in complete system freeze and hard reboot.
**Prevention:** Never run massive, multi-stage installation scripts blindly as a single bash block. Always serialize heavy tasks:
1. `apt-get` / Snaps
2. `cargo install` (single threaded or serialized)
3. Large network pulls (`ollama`). 

## 2. Python PEP 668 "Externally Managed Environment"
**Error:** Running `pip3 install --user pipx` fails on modern Ubuntu (24.04+) with `error: externally-managed-environment`.
**Prevention:** Never use `pip install --user` globally on Ubuntu. Always use `sudo apt-get install -y pipx` for pipx, and then use `pipx install <package>` for tools.

## 3. GNOME Wayland GUI App Crashing
**Error:** Starting `ulauncher` via a background terminal task (`nohup ulauncher &`) resulted in silent crashes because the headless agent terminal lacked `WAYLAND_DISPLAY` and the graphical DBus session.
**Prevention:** To autostart or launch GUI apps persistently, always bind them to the user's actual graphical session using `systemd`: `systemctl --user enable --now <app>.service`.

## 4. Keybinding Conflicts (IBus vs GNOME)
**Error:** Mapping `<Super>space` to a custom GNOME shortcut failed because Ubuntu's underlying IBus (Input Method) framework intercepts the keystroke at a lower kernel layer.
**Prevention:** Always clear the IBus hotkey (`gsettings set org.freedesktop.ibus.general.hotkey triggers "[]"`) before attempting to bind `<Super>space` in GNOME.

## 5. NPM 404 Missing Packages
**Error:** `npm install -g @opencode/opencode` threw a 404 Not Found error and halted the setup sequence.
**Prevention:** Never let a single missing NPM package crash a massive sequence. Always append `|| true` to non-critical tool installations and verify package existence before halting.

## 6. Antigravity Token Exhaustion (2026-06-13)
**Error:** All Antigravity API quotas reached N/A — Gemini, Claude, GPT-OSS all showed 0 remaining with reset times of 8m–4h. The `antigravity` IDE language server and dashboard `/api/ask` (which was calling `gemini-2.5-flash` directly) consumed the full token budget.
**Prevention:** Never call premium model APIs directly through paid keys. Always route through freellmapi proxy (`http://localhost:3001/v1`) which uses auto-failover across 12 free providers. The dashboard `/api/ask` now uses freellmapi. Also watch for git hooks triggering vector DB re-seeds (heavy but local/ free).
