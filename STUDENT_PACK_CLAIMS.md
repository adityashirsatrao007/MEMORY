# GitHub Student Pack — Claim Checklist

**Account:** adityashirsatrao007
**Time needed:** ~15 minutes

---

## Step 1: Verify Education Status
https://github.com/settings/education/benefits
- [ ] Sign in with GitHub
- [ ] Verify student status with .edu email or student ID
- [ ] Wait for approval (usually instant)

---

## Step 2: Claim Benefits (in order of value)

### DigitalOcean — $200 credit
1. Go to: https://www.digitalocean.com/education/
2. Click "Claim your $200 credit"
3. Sign in with GitHub
4. Create account
5. Save API key from: https://cloud.digitalocean.com/account/api/tokens
6. Run: `echo "DIGITALOCEAN_API_KEY=<key>" >> ~/.config/global-apikeys/keys.env`

### MongoDB Atlas — $50 + free cert
1. Go to: https://www.mongodb.com/community/forums/c/academia/students/42
2. Sign up with GitHub
3. Create free M0 cluster at: https://cloud.mongodb.com
4. Get connection string from cluster → Connect → Drivers
5. Run: `echo "MONGODB_URI=<uri>" >> ~/.config/global-apikeys/keys.env`

### Clerk — Free Pro
1. Go to: https://clerk.com/education
2. Sign in with GitHub
3. Create application
4. Copy Publishable Key + Secret Key from dashboard
5. Run:
   ```
   echo "CLERK_PUBLISHABLE_KEY=pk_..." >> ~/.config/global-apikeys/keys.env
   echo "CLERK_SECRET_KEY=sk_..." >> ~/.config/global-apikeys/keys.env
   ```

### Stripe — No fees on first $1000
1. Go to: https://stripe.com/education
2. Sign up with GitHub
3. Get test keys from: https://dashboard.stripe.com/test/apikeys
4. Run:
   ```
   echo "STRIPE_SECRET_KEY=sk_test_..." >> ~/.config/global-apikeys/keys.env
   echo "STRIPE_PUBLISHABLE_KEY=pk_test_..." >> ~/.config/global-apikeys/keys.env
   ```

### Datadog — Free 2 years
1. Go to: https://www.datadoghq.com/student/
2. Sign up with GitHub
3. Get API key from: https://app.datadoghq.com/account/settings#api
4. Run: `echo "DD_API_KEY=<key>" >> ~/.config/global-apikeys/keys.env`

### Heroku — $13/month for 24 months
1. Go to: https://www.heroku.com/github-student
2. Sign in with GitHub
3. Get API key from: https://dashboard.heroku.com/account
4. Run: `echo "HEROKU_API_KEY=<key>" >> ~/.config/global-apikeys/keys.env`

### JetBrains — Free IDEs
1. Go to: https://www.jetbrains.com/student/
2. Sign in with GitHub
3. Download: https://www.jetbrains.com/student/#discounts
4. Activate in IDE: Help → Register → JB Student

### FrontendMasters — 6 months free
1. Go to: https://frontendmasters.com/github-student-pack/
2. Sign in with GitHub
3. Access courses at: https://frontendmasters.com

### GitHub Copilot
1. Go to: https://github.com/settings/copilot
2. Enable Copilot
3. Install VS Code extension: GitHub.copilot
4. Already configured: `.github/copilot-instructions.md` → reads MEMORY

### GitHub Codespaces
1. Go to: https://github.com/codespaces
2. Create codespace on MEMORY repo
3. Pre-configured: `.devcontainer/devcontainer.json`

### Notion — Free education plan
1. Go to: https://www.notion.so/product/notion-for-education
2. Sign up with .edu email
3. Get AI features included

### Termius — Free SSH
1. Go to: https://termius.com/education
2. Sign up with GitHub
3. Install: https://termius.com/download

---

## Step 3: Verify All Keys
```bash
source ~/.config/global-apikeys/load_keys.sh
echo "Keys loaded:"
env | grep -E "DIGITALOCEAN|MONGODB|CLERK|STRIPE|DD_API|HEROKU" | sed 's/=.*/=***/'
```

---

## Step 4: Test Integrations
```bash
cd ~/Desktop/Projects/MEMORY
make infra           # Start vector DB API
memory-search "test" # Search vector DB
make tool-check      # Verify all tools
```

---

## Credit Expiration Summary

| Benefit | Credit | Expires |
|---------|--------|---------|
| DigitalOcean | $200 | 2026-07-31 |
| MongoDB | $50 | Never (M0 free tier) |
| Datadog | Free Pro | 2 years from claim |
| Heroku | $13/mo | 24 months from claim |
| Stripe | $1000 no fees | Until used |
| Copilot | Free | While student |
| Codespaces | 120 hrs/mo | While student |
| JetBrains | Free IDEs | While student |
| FrontendMasters | 6 months | From claim |
| Notion | Free plan | While student |
| Termius | Free Pro | While student |
