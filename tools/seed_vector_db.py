"""Seed ChromaDB with all module files (GEMINI.md + modules).
Run with --force to re-seed even if entries exist or content unchanged."""

import chromadb
import hashlib
import os
import sys
from pathlib import Path

BASE = Path(os.path.expanduser("~/Desktop/Projects/MEMORY"))
VECTOR_DB_PATH = BASE / "memory" / "vector_db"
FILES = [
    BASE / "GEMINI.md",
    *(BASE / "memory/modules").glob("*.md"),
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

if "--force" in sys.argv:
    try:
        client.delete_collection("antigravity_memory")
    except Exception:
        pass

collection = client.get_or_create_collection(name="antigravity_memory")

existing = collection.get()
if existing and existing.get("ids") and "--force" not in sys.argv:
    current_hash = compute_hash()
    if HASH_FILE.exists() and HASH_FILE.read_text().strip() == current_hash:
        print(f"  Content unchanged ({len(existing['ids'])} entries). Skipping re-seed.")
        sys.exit(0)
    print(f"  Content changed. Re-seeding ({len(existing['ids'])} old entries).")
    try:
        client.delete_collection("antigravity_memory")
        collection = client.get_or_create_collection(name="antigravity_memory")
    except Exception:
        pass

all_chunks = []
for fpath in sorted(FILES):
    all_chunks.extend(chunk_file(fpath))

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

collection.add(documents=documents, metadatas=metadatas, ids=ids)
HASH_FILE.write_text(compute_hash())
print(f"  Seeded {len(ids)} chunks from {len(FILES)} files into vector DB")
