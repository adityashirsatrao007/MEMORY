# DevOps, CI/CD & Infrastructure

## Docker Best Practices
```dockerfile
# Multi-stage build for small images
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

### Rules
- Always use `.dockerignore` — never copy `.git`, `node_modules`, `.venv`, `vector_db`
- Pin base image versions: `python:3.12.4-slim`, not `python:latest`
- Run as non-root: `RUN adduser --disabled-password appuser && USER appuser`
- Use `COPY` not `ADD` (unless tar extraction needed)
- Layer cache: copy `requirements.txt` before source code

## GitHub Actions CI/CD

### Standard Pipeline
```yaml
name: CI
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install ruff mypy pytest
      - run: ruff check .
      - run: mypy .
      - run: pytest tests/ -v
```

### MEMORY-Specific CI
```yaml
  validate-memory:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install chromadb
      - run: make validate
      - run: make seed
      - run: make evals
```

### Rules
- Never commit secrets — use `secrets.GITHUB_TOKEN`
- Cache dependencies: `actions/cache@v4`
- Pin action versions: `actions/checkout@v4`, not `@main`
- Fail fast: `fail-fast: true` in matrix builds
- Run on PR + push to main, never on tags-only

## PM2 Process Management
```bash
# Start app
pm2 start app.js --name "memory-api"

# Start with cluster mode
pm2 start app.js -i max --name "memory-api"

# Monitor
pm2 monit

# Logs
pm2 logs memory-api --lines 50

# Restart on file change
pm2 start app.js --watch

# Save process list
pm2 save

# Auto-start on reboot
pm2 startup
```

## Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name memory.example.com;

    location / {
        proxy_pass http://127.0.0.1:8083;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8082;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Systemd Service
```ini
[Unit]
Description=MEMORY Dashboard
After=network.target

[Service]
Type=simple
User=aditya
WorkingDirectory=/home/aditya/Desktop/Projects/MEMORY
ExecStart=/home/aditya/Desktop/Projects/MEMORY/.venv/bin/python tools/dashboard.py
Restart=always
RestartSec=5
Environment=MEMORY_ROOT=/home/aditya/Desktop/Projects/MEMORY
Environment=MEMORY_NON_COMMERCIAL=1

[Install]
WantedBy=multi-user.target
```

## Deployment Checklist
- [ ] All tests pass: `make test`
- [ ] Lint clean: `make lint`
- [ ] No secrets in diff: `git diff | gitleaks detect --no-git`
- [ ] Health endpoint works: `curl /health`
- [ ] Ready endpoint works: `curl /ready`
- [ ] CORS configured for production domain
- [ ] SIGTERM handler installed (Node.js)
- [ ] CSP headers set (Express/FastAPI)
- [ ] Rate limiting enabled
- [ ] Logging to stdout (not files) for containers
