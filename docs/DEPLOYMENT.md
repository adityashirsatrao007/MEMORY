# Deployment

## GitHub Pages

The site auto-deploys via GitHub Actions on push to `main`:

1. Push to `main` → triggers `.github/workflows/gh-pages.yml`
2. Pages builds with `actions/configure-pages@v5`
3. Deploys to `https://adityashirsatrao007.github.io/MEMORY/`

## Self-Hosted (Any Server)

```bash
# Clone on your server
git clone https://github.com/adityashirsatrao007/MEMORY.git /opt/memory

# Set up environment
cd /opt/memory
python3 -m venv .venv
source .venv/bin/activate
pip install chromadb

# Initialize
make all

# Serve docs (optional)
cd docs
python3 -m http.server 8080
```

## Docker (Coming Soon)

```dockerfile
FROM python:3.12-slim
WORKDIR /memory
COPY . .
RUN pip install chromadb && make validate
CMD ["make", "seed"]
```

## CI/CD Integration

The `Makefile` provides all hooks needed for CI:
- `make validate` — module structure + symlink integrity
- `make seed` — vector DB seeding
- `make stats` — module metrics
