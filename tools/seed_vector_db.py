# Copyright (c) 2026 Aditya Shirsatrao
# MIT License — see LICENSE file.

"""Seed ChromaDB with all module files (GEMINI.md + modules).
Run with --force to re-seed even if entries exist or content unchanged."""

import chromadb

import hashlib
import os
import sys
from pathlib import Path

BASE = Path(os.environ.get("MEMORY_ROOT", os.getcwd()))
VECTOR_DB_PATH = BASE / "memory" / "vector_db"
FILES = [
    BASE / "GEMINI.md",
    *(BASE / "memory/modules").glob("*.md"),
    BASE / ".agent-progress.md",
    BASE / "memory/memory-bank/progress.md",
    BASE / "memory/memory-bank/activeContext.md",
    BASE / "memory/memory-bank/architecture.md",
    BASE / "memory/memory-bank/decisions.md",
    BASE / "memory/memory-bank/walkthrough.md",
    # Skills indexed via BM25/rg for instant text search (not embeddings)
]
HASH_FILE = VECTOR_DB_PATH / "content_hash"

def compute_hash():
    h = hashlib.sha256()
    for fpath in sorted(FILES):
        if fpath.exists():
            h.update(fpath.read_bytes())
    return h.hexdigest()

def chunk_file(path):
    with open(path) as f:
        lines = f.readlines()
    chunks = []
    current_section = f"file:{path.name}"
    current_chunk = []
    line_start = 1
    for i, line in enumerate(lines, 1):
        if line.startswith("## ") or line.startswith("# "):
            if current_chunk:
                chunks.append((current_section, "".join(current_chunk), line_start, i - 1, str(path)))
            current_section = line.strip("# \n")
            current_chunk = [line]
            line_start = i
        else:
            current_chunk.append(line)
    if current_chunk:
        chunks.append((current_section, "".join(current_chunk), line_start, len(lines), str(path)))
    return chunks

client = chromadb.PersistentClient(path=str(VECTOR_DB_PATH))

COLLECTION_NAME = "antigravity_memory"

if "--force" in sys.argv:
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

collection = client.get_or_create_collection(name=COLLECTION_NAME)

existing = collection.get()
if existing and existing.get("ids") and "--force" not in sys.argv:
    current_hash = compute_hash()
    if HASH_FILE.exists() and HASH_FILE.read_text().strip() == current_hash:
        print(f"  Content unchanged ({len(existing['ids'])} entries). Skipping re-seed.")
        sys.exit(0)
    print(f"  Content changed. Re-seeding ({len(existing['ids'])} old entries).")
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

collection = client.get_or_create_collection(name=COLLECTION_NAME)

all_chunks = []
for fpath in sorted(FILES):
    if not fpath.exists():
        continue
    c = chunk_file(fpath)
    all_chunks.extend(c)
    print(f"  {fpath.name}: {len(c)} chunks", flush=True)

ids, documents, metadatas = [], [], []
for i, (section, text, start, end, src) in enumerate(all_chunks):
    if len(text.strip()) < 20:
        continue
    ids.append(f"chunk-{i:04d}")
    documents.append(text)
    metadatas.append({
        "source": src,
        "section": section,
        "lines": f"{start}-{end}",
        "file": Path(src).name,
    })

if ids:
    BATCH_SIZE = 1000
    for b in range(0, len(ids), BATCH_SIZE):
        collection.add(
            documents=documents[b:b+BATCH_SIZE],
            metadatas=metadatas[b:b+BATCH_SIZE],
            ids=ids[b:b+BATCH_SIZE]
        )
        print(f"  Indexed {min(b+BATCH_SIZE, len(ids))}/{len(ids)} chunks", flush=True)

HASH_FILE.write_text(compute_hash())
print(f"  Seeded {len(ids)} chunks from {len(FILES)} files into vector DB")
