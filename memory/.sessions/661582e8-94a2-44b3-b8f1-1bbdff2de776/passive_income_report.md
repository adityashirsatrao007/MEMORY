# 💰 Passive Income Master Report — Aditya's Setup
> Generated: June 14, 2026 | Source: money4band repo + honeygain-ovpn analysis

## Your Network Reality
- **ISP Type:** CGNAT (double NAT) — shared public IP
- **Hardware:** AMD Ryzen 5 4600H + NVIDIA GTX 1650 Ti + 30GB RAM
- **Key constraint:** Inbound connections blocked → Pawns-style apps fail
- **Good news:** All outbound-tunnel apps work fine ✅

---

## 📋 Full App Compatibility Matrix

| App | Works Behind CGNAT? | Type | Pay Rate | Your Status |
|-----|-------------------|------|----------|-------------|
| **Honeygain** | ✅ Yes | Bandwidth (outbound) | ~$1/GB | ✅ Running |
| **PacketStream** | ✅ Yes | Bandwidth (outbound) | $0.10/GB | ✅ Just Installed |
| **EarnApp** | ✅ Yes | Bandwidth (outbound) | ~$0.30–1/GB | ❌ Not installed |
| **Peer2Profit** | ✅ Yes | Bandwidth (outbound) | ~$1/GB | ❌ Not installed |
| **Repocket** | ✅ Yes | Bandwidth (outbound) | ~$1/GB | ❌ Not installed |
| **Earnfm** | ✅ Yes | Bandwidth (outbound) | ~$0.25/GB | ❌ Not installed |
| **Proxylite** | ✅ Yes | Bandwidth (outbound) | ~$0.5/GB | ❌ Not installed |
| **Bitping** | ✅ Yes | Network monitoring | ~$0.1–0.5/hr | ❌ Not installed |
| **Grass** | ✅ Yes | Web scraping proxy | varies | ❌ Not installed |
| **Packetshare** | ✅ Yes | Bandwidth (outbound) | ~$0.5/GB | ❌ Not installed |
| **Folding@Home** | ✅ Yes (compute) | Protein folding → BAN | BAN tokens | ✅ Running |
| **IPRoyal Pawns** | ❌ CGNAT blocks | Bandwidth (inbound) | $0.20/GB | ❌ Removed |
| **Proxyrack** | ⚠️ Partial | Bandwidth | varies | Skip |
| **Gradient** | ⚠️ Uncertain | AI compute/bandwidth | varies | Try later |
| **Wipter** | ⚠️ Uncertain | Bandwidth | varies | Try later |

---

## 🏆 Priority Install List (Best ROI for Your Setup)

### 1. EarnApp — HIGH PRIORITY ⭐
- **Docker image:** `fazalfarhan01/earnapp:lite`
- Needs: UUID (generated) + account on earnapp.com
- **Pay:** Best rates among all bandwidth apps (~$0.50–1.50/GB)
- **Sign up:** https://earnapp.com/i/sdk-node-xxx (use referral for bonus)

### 2. Peer2Profit — HIGH PRIORITY ⭐
- **Docker image:** `peer2profit/peer2profit_linux`
- Needs: Email only
- **Pay:** ~$1/GB, paid in crypto (USDT)
- **Sign up:** https://peer2profit.com

### 3. Repocket — MEDIUM PRIORITY
- **Docker image:** `repocket/repocket`
- Needs: Email + API key
- **Pay:** ~$1/GB
- **Sign up:** https://link.repocket.co/rL9e

### 4. Earnfm — MEDIUM PRIORITY
- **Docker image:** `earnfm/earnfm-client`
- Needs: API token
- **Pay:** ~$0.25/GB
- **Sign up:** https://earn.fm/ref/XXXXX

### 5. Bitping — LOW-MEDIUM
- **Docker image:** `bitping/bitpingd`
- Pays for uptime monitoring, not bandwidth
- Less dependent on traffic volume
- **Sign up:** https://app.bitping.com

---

## 🍯 Honeygain OVPN Trick — My Verdict

### What it does:
Runs **multiple Honeygain Docker containers**, each through a different VPN endpoint (OpenVPN), making them appear as separate devices from different countries. The creator earns ~$9/month from 8 containers on a $1/month Google Cloud VM.

### ⚠️ SKIP THIS — Here's why:

| Risk | Severity |
|------|----------|
| Honeygain detects datacenter IPs → blocks earnings | 🔴 High |
| Most VPN providers flagged as DCH (datacenter) — earns $0 | 🔴 High |
| Honeygain HAC anti-cheat system → permanent account ban | 🔴 High |
| Your CGNAT already shares IP → "Network overused" errors possible | 🟡 Medium |
| Requires running a cheap VPS + VPN subscription | 🟡 Cost |

### ✅ Safe Honeygain boosts instead:
1. **JumpTask mode** — 10% earnings bonus, toggle in dashboard
2. **Referrals** — Earn % of referral's earnings passively
3. **Keep 24/7 uptime** — Honeygain rewards consistent connections

---

## 🚀 What I Recommend Installing Next

### EarnApp (easiest, best rates):
```bash
# 1. Generate a UUID
UUID=$(cat /proc/sys/kernel/random/uuid)
echo "Your UUID: $UUID"

# 2. Register this UUID at: https://earnapp.com/r/sdk-node-$UUID

# 3. Run the container
docker run -d --restart=always \
  --name earnapp \
  -e EARNAPP_UUID=sdk-node-$UUID \
  fazalfarhan01/earnapp:lite
```

### Peer2Profit:
```bash
docker run -d --restart=always \
  --name peer2profit \
  -e P2P_EMAIL=adityashirsatrao007@gmail.com \
  peer2profit/peer2profit_linux:latest
```

### Repocket:
```bash
# First: sign up at repocket.co and get API key
docker run -d --restart=always \
  --name repocket \
  -e RP_EMAIL=adityashirsatrao007@gmail.com \
  -e RP_API_KEY=YOUR_API_KEY \
  repocket/repocket
```

---

## 💸 Total Earning Potential (Realistic Estimate)

| Service | Monthly Est. | Notes |
|---------|-------------|-------|
| Honeygain | $0.40–0.80 | Already running, CGNAT limits traffic |
| PacketStream | $0.20–0.50 | Just installed |
| EarnApp | $0.50–2.00 | Best rates, install next |
| Peer2Profit | $0.30–1.00 | Install after EarnApp |
| Repocket | $0.20–0.80 | Install after P2P |
| Folding@Home | ~50 BAN/mo | GPU helps a lot |
| **TOTAL** | **~$2–5/month** | On CGNAT with limited traffic |

> Note: With a real public IP (static), this could be 3–5x higher (~$10–15/month).
> The fundamental limit is CGNAT reducing how much traffic flows through you.

---

## 🔑 Keys to save after signup
Add to `/home/aditya/.config/global-apikeys/keys.env`:
```
EARNAPP_UUID=sdk-node-XXXX
PEER2PROFIT_EMAIL=adityashirsatrao007@gmail.com
REPOCKET_EMAIL=adityashirsatrao007@gmail.com
REPOCKET_API_KEY=XXXX
EARNFM_API_TOKEN=XXXX
```
