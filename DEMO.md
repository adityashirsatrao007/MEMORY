# Demo

## Quick Start (2 minutes)

```bash
# Clone and install
git clone https://github.com/adityashirsatrao007/MEMORY.git
cd MEMORY
make all

# Symlink for your agent
ln -sf $PWD/GEMINI.md CLAUDE.md
```

## What to Try

### 1. Search memory
Your agent will automatically find relevant context via ChromaDB. Try asking it about any topic covered in the 12 modules.

### 2. Check module stats
```bash
make stats
```

### 3. Validate the setup
```bash
make validate
```

### 4. Seed vector DB
```bash
make seed
```

## Architecture Walkthrough

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full architecture diagram and module descriptions.

## Video Demo

*(Coming soon)*
