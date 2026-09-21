# RESOURCES Toolbox — Deep Usage Guide

All starred repos are cloned to `~/Desktop/Projects/RESOURCES/<name>` (shallow). This module documents how to get maximum value out of each one for Aditya's stack (full-stack, ML, security, data, freelancing).

## yt-dlp (YouTube/media downloader) — PRIMARY TOOL
- Binary: `yt-dlp` (installed globally via pipx, v2026.07.04).
- Wrapper: `~/bin/ytdl` with presets:
  - `ytdl <url>` → video, best quality, mp4 merge
  - `ytdl <url> -q 720p` → capped quality
  - `ytdl <url> --audio-only` → mp3 320k
  - `ytdl <url> --audio-only -q 128k` → lower bitrate
- Wrapper always honors the YouTube/Media Link Protocol (ask intent + quality first, see `01-core-rules.md`).
- Useful extras beyond simple download:
  - `yt-dlp -J --no-playlist <url>` → JSON metadata (title, duration, uploader, chapters) — great for content research, summaries, dataset building.
  - `--write-subs --sub-langs en --sub-format srt` → subtitles for language learning / dataset extraction.
  - `--download-sections "*00:00-05:00"` → clip a segment (great for creating short datasets or quotes).
  - `-f "bestaudio[ext=m4a]"` → bandwidth-efficient audio for podcasts/voice datasets.

## Nitro 3 (universal server toolkit)
- Framework repo for READING source/builds. To build new servers: `npx nitro@latest` then `nitro dev|build|deploy`.
- Value: deploy the same JS server to Node, Deno, Bun, Vercel, Cloudflare Workers, etc. Great for AI backends that must run serverless + edge (SentinelX-style APIs).
- Local pnpm: `pnpm` (v9.15.9, wrapper at `~/bin/pnpm`; Node 20 compatible). npm prefix is `/usr` (root-only) — do NOT try `npm i -g`, use corepack pnpm or pipx instead.
- Deep usage: read `nitro/examples/` for pattern references; extract templates into `$MEMORY_ROOT/templates/` when building server listeners.

## authentik (SSO / IdP)
- Run-on-demand; requires docker compose + Postgres + Redis + worker (multi-GB). Do not pull images lazily.
- Value: self-hosted SSO for internal tools — OIDC/SAML/LDAP provisioning + MFA + rate limiting. Fits security/Threat-Intel portfolio and building demo dashboards with real auth.
- Setup path when needed:
  1. `cd ~/Desktop/Projects/RESOURCES/authentik`
  2. follow `docker-compose.yml` + `.env` override from repo README (copy `.env` sample)
  3. `docker compose up -d` (web on :9000, core on :9443)
- Never expose without TLS in production; it IS an auth product, so secrets/handling rules apply strictly.

## go-whatsapp-web-multidevice (WhatsApp REST API)
- Go module; build the binary with `go build` in its root. Provides REST endpoints for sending/receiving WhatsApp messages with multi-device support + webhooks + (MCP mention in description).
- Value: WhatsApp automation for freelancing client contact, alerts (threat intel to SOC channels), or the n8n/MCP pipeline.
- Caveats: WhatsApp-ToS-sensitive; only use for legitimate botting where allowed. Do not use for spam.
- MCP relevance: repo mentions MCP support — a real integration angle for the memory server if needed.

## JUCE (C++ audio framework)
- Requires CMake (>3.15) + C++ compiler (g++ present) to build. Heavy; reference-only unless Aditya does audio work (VST/AU plugins).
- Value: if he ever extends the "spoken Japanese study app" or does audio DSP, JUCE is the canonical framework.
- No build performed yet (no active audio project). Revisit on demand.

## trackerslist (BitTorrent tracker list)
- Plain data, zero build. Files: `trackerslist/trackers_all.txt` (226 trackers), plus http/udp/ws variants.
- Value: usable directly as data for pipeline tests, or in qBittorrent/arr-stack config for media automation.
- This is reference data only — not software to install.
- **POWERED BY**: aria2 runs with all 226 trackers loaded via `--bt-tracker`. qBittorrent-nox WebUI also wired. See `01-core-rules.md` → "Torrent/Media Download Toolbox".

## free-for-dev (SaaS/PaaS/IaaS free tiers)
- Markdown reference list. Search it when choosing infra for a project: `rg "Postgres|Redis|CI|storage" ~/Desktop/Projects/RESOURCES/free-for-dev/README.md`.
- Value: build freelancing products at $0 until they earn. Always check this before suggesting paid services to Aditya.
## Anime (Crunchyroll, official)
- `~/bin/crunchy` (crunchy-cli v3.6.7) + `~/bin/anime` wrapper. Official Crunchyroll client — the ONLY legal CLI path. Requires user's own account (`anime login`) or `--anonymous` free tier.
- Full usage in `01-core-rules.md` → "Anime Downloader/Streamer".
