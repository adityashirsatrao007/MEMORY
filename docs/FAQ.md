# Frequently Asked Questions

## General

**What is MEMORY?**
A modular, cross-agent knowledge system that replaces monolithic agent config files with 12 load-on-demand modules backed by ChromaDB vector search. Your agents use 60-95% fewer tokens per session.

**Is it free?**
Yes for personal/non-commercial use (set `MEMORY_NON_COMMERCIAL=1`). Commercial use requires an activation key from [pricing.html](pricing.html).

**Which agents does it work with?**
Claude Code, OpenCode, Cursor, Windsurf, GitHub Copilot, and Cline — any agent that reads a config file from the project root.

## Technical

**How much memory does it use?**
Lazy init: 48 MB RAM, 2% CPU. Full init: 124 MB, 5% CPU. ChromaDB seed: 256 MB, 15% CPU.

**How long does vector search take?**
~0.8 seconds average. 94.2% recall rate across all 12 modules.

**Can I add my own modules?**
Yes. Create `memory/modules/13-my-module.md` and run `make seed` to index it in ChromaDB.

**Do I need API keys?**
For the free tier, no — the freellmapi proxy routes across 16 free providers. For production, configure your keys in `~/.config/global-apikeys/keys.env`.

## Commercial

**Can I pay in INR?**
Yes. We accept USD and INR via UPI, wire, PayPal, and crypto.

**Is there a refund policy?**
Full refund within 30 days of purchase.

**Can I try before buying?**
Get a free trial key from [pricing.html](pricing.html). The source is fully visible on GitHub — try everything, then purchase when you need commercial use.
