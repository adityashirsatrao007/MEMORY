#!/usr/bin/env python3
"""Seed ChromaDB with modules + skill summaries.
Run with --force to re-seed. Run with --skills-only to seed only skills.
Run with --modules-only to seed only modules (original behavior)."""
import chromadb
import hashlib
import os
import re
import sys
from pathlib import Path

BASE = Path(os.environ.get("MEMORY_ROOT", os.getcwd()))
VECTOR_DB_PATH = BASE / "memory" / "vector_db"
SKILL_DIR = BASE / ".agents" / "skills"

MODULE_FILES = [
    BASE / "GEMINI.md",
    *(BASE / "memory/modules").glob("*.md"),
    BASE / ".agent-progress.md",
    BASE / "memory/memory-bank/progress.md",
    BASE / "memory/memory-bank/activeContext.md",
    BASE / "memory/memory-bank/architecture.md",
    BASE / "memory/memory-bank/decisions.md",
    BASE / "memory/memory-bank/walkthrough.md",
]

HASH_FILE = VECTOR_DB_PATH / "content_hash"
COLLECTION_NAME = "antigravity_memory"


def compute_hash():
    h = hashlib.sha256()
    for fpath in sorted(MODULE_FILES):
        if fpath.exists():
            h.update(fpath.read_bytes())
    # Include skill count in hash
    skill_count = len(list(SKILL_DIR.glob("*/SKILL.md"))) if SKILL_DIR.exists() else 0
    h.update(str(skill_count).encode())
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


def parse_frontmatter(content: str) -> dict:
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            val = val.strip().strip('"').strip("'")
            if val:
                fm[key.strip()] = val
    return fm


def chunk_skill(skill_path: Path):
    """Create a single chunk per skill: name + description + first 10 lines."""
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return None
    
    content = skill_file.read_text(errors='replace')
    fm = parse_frontmatter(content)
    name = fm.get('name', skill_path.name)
    desc = fm.get('description', '')
    
    # Get first 10 non-frontmatter lines
    lines = content.split('\n')
    body_lines = []
    in_fm = False
    past_fm = False
    for line in lines:
        if line.strip() == '---':
            if not in_fm:
                in_fm = True
            else:
                past_fm = True
            continue
        if in_fm and not past_fm:
            continue
        if line.strip() and not line.startswith('#'):
            body_lines.append(line.rstrip())
            if len(body_lines) >= 10:
                break
    
    body = '\n'.join(body_lines)
    document = f"Skill: {name}\nDescription: {desc}\n\n{body}"
    
    return {
        'id': f"skill-{skill_path.name}",
        'document': document,
        'metadata': {
            'source': str(skill_file),
            'section': f"skill:{name}",
            'lines': '1-15',
            'file': 'SKILL.md',
            'skill_name': skill_path.name,
            'type': 'skill',
        }
    }


def main():
    force = '--force' in sys.argv
    skills_only = '--skills-only' in sys.argv
    modules_only = '--modules-only' in sys.argv
    
    client = chromadb.PersistentClient(path=str(VECTOR_DB_PATH))
    
    if force:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    
    existing = collection.get()
    if existing and existing.get("ids") and not force:
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
    
    all_ids, all_docs, all_meta = [], [], []
    
    # Module chunks
    if not skills_only:
        print("--- Indexing modules ---")
        for fpath in sorted(MODULE_FILES):
            if not fpath.exists():
                continue
            c = chunk_file(fpath)
            print(f"  {fpath.name}: {len(c)} chunks", flush=True)
            for i, (section, text, start, end, src) in enumerate(c):
                if len(text.strip()) < 20:
                    continue
                all_ids.append(f"mod-{len(all_ids):05d}")
                all_docs.append(text)
                all_meta.append({
                    'source': src,
                    'section': section,
                    'lines': f'{start}-{end}',
                    'file': Path(src).name,
                    'type': 'module',
                })
    
    # Skill chunks
    if not modules_only:
        print("--- Indexing skills ---")
        if SKILL_DIR.exists():
            skill_files = sorted(SKILL_DIR.glob("*/SKILL.md"))
            print(f"  Found {len(skill_files)} skills", flush=True)
            for i, sf in enumerate(skill_files):
                skill_path = sf.parent
                chunk = chunk_skill(skill_path)
                if chunk is None:
                    continue
                all_ids.append(chunk['id'])
                all_docs.append(chunk['document'])
                all_meta.append(chunk['metadata'])
                if (i + 1) % 500 == 0:
                    print(f"  Indexed {i+1}/{len(skill_files)} skills", flush=True)
            print(f"  Indexed {len(skill_files)} skills total", flush=True)
        else:
            print(f"  Skill dir not found: {SKILL_DIR}")
    
    # Batch insert
    if all_ids:
        BATCH_SIZE = 1000
        for b in range(0, len(all_ids), BATCH_SIZE):
            collection.add(
                documents=all_docs[b:b+BATCH_SIZE],
                metadatas=all_meta[b:b+BATCH_SIZE],
                ids=all_ids[b:b+BATCH_SIZE]
            )
            print(f"  Indexed {min(b+BATCH_SIZE, len(all_ids))}/{len(all_ids)} chunks", flush=True)
    
    HASH_FILE.write_text(compute_hash())
    
    # Stats
    mod_count = sum(1 for m in all_meta if m.get('type') == 'module')
    skill_count = sum(1 for m in all_meta if m.get('type') == 'skill')
    print(f"\n  Total: {len(all_ids)} chunks ({mod_count} modules + {skill_count} skills)")
    print(f"  Collection: {COLLECTION_NAME}")


if __name__ == '__main__':
    main()
