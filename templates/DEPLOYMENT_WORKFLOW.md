# Deployment Workflow Template

Use this template for every project deployment. Copy to `.github/workflows/deploy.yml`.

## GitHub Actions + Vercel / Fly.io

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: make setup
      - name: Lint, typecheck, test
        run: make ci
      - name: Build
        run: make build
      - name: Deploy
        run: make deploy
```

## Phase Gate Checklist

| Gate | Check | Block on |
|------|-------|----------|
| Pre-deploy | `make ci` passes | lint/typecheck/test failures |
| Build | `make build` succeeds | compile errors, missing assets |
| Staging | Smoke test + E2E | failing critical paths |
| Canary | 5% traffic for 24h | error rate > 0.1% |
| Production | Full rollout | monitor for 1h after deploy |

## Rollback

```bash
# Vercel
vercel rollback <deployment-id> --yes

# Fly
fly deploy --image <previous-image-tag>

# Kubernetes
kubectl rollout undo deployment/<name>
```
