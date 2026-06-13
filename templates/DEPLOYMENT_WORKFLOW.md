# Instant Publish — GitHub + Vercel Deployment

> Zero-hiccup workflow for pushing web projects live

---

## PRE-FLIGHT CHECKS

```bash
# Verify tools installed + authenticated
gh auth status 2>&1
vercel whoami 2>&1
```

If NOT installed:
```bash
# GitHub CLI
sudo apt install gh
gh auth login --web --git-protocol https

# Vercel CLI
npm i -g vercel
vercel login
```

---

## DEPLOYMENT WORKFLOW

### Step 1: Prepare Project

```bash
# Move static assets to public/ (Vite/React critical)
mkdir -p public
find . -maxdepth 1 -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.svg" -o -name "*.ico" -o -name "*.webp" \) ! -path "./node_modules/*" -exec cp {} public/ \;

# Check for env vars
grep -rn 'import.meta.env\|process.env\|VITE_' --include="*.ts" --include="*.tsx" . | grep -v node_modules | head -20

# Build test
npm run build 2>&1

# Verify .gitignore
cat .gitignore | grep -E "node_modules|dist|.vercel|.env"
```

### Step 2: Create GitHub Repo + Push

```bash
# Initialize if not already
git init && git add -A && git commit -m "feat: initial commit"

# Create repo + push (public for Vercel free tier)
env -u GITHUB_TOKEN gh repo create my-project --public --source=. --push --description "Project description"
```

### Step 3: Deploy to Vercel

```bash
# One command — auto-detects framework, links repo, deploys
vercel --yes --prod
```

### Step 4: Set Environment Variables (if needed)

```bash
vercel env add VARIABLE_NAME production
# Paste value when prompted

# Redeploy with env vars
vercel --prod
```

### Step 5: Verify

Output shows Production URL + Inspect URL. Check:
- Page loads without errors
- Images display correctly
- No console errors
- Layout correct on mobile + desktop

---

## REPORT TO USER

```
Website Published Successfully!

Live URL:         https://my-project.vercel.app
GitHub Repo:      https://github.com/USERNAME/my-project
Deployment:       READY
Framework:        Next.js / Vite / etc.
Auto-Deploy:      Enabled (pushes to main auto-deploy)
```

---

## UPDATES (Already Deployed)

```bash
git add -A && git commit -m "fix: description" && git push origin main
# Vercel auto-redeploys within ~15 seconds
```

---

## ERROR REFERENCE

| Error | Fix |
|-------|-----|
| Unable to add remote "origin" | `git remote set-url origin NEW_URL` |
| Broken images on Vercel | Move static assets to `public/` |
| gh: not found | `sudo apt install gh` |
| vercel: command not found | `npm i -g vercel` |
| Build fails on Vercel | Run `npm run build` locally first |
| Env vars not available | `vercel env add VARNAME production` |
| 404 on SPA refresh | Add `vercel.json` rewrites |

### Vite SPA Rewrites
```json
{ "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }] }
```

### Next.js Notes
- API routes work automatically as serverless functions
- Image optimization works out of the box
- `output: 'export'` needs output directory set in Vercel

---

## QUICK REFERENCE (3-Step Deploy)

```bash
# 1. Create GitHub repo + push
env -u GITHUB_TOKEN gh repo create my-project --public --source=. --push

# 2. Deploy to Vercel
vercel --yes --prod

# 3. Done! Future updates:
git add -A && git commit -m "update" && git push origin main
```
