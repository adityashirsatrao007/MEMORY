#!/usr/bin/env python3
"""MCP Memory Server — persistent shared memory for any agent (opencode, agy, etc.).

Every agent connects on startup → gets full context automatically.
Backed by $MEMORY_ROOT/memory/ with ChromaDB vector search + plain markdown.
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path

MEMORY_ROOT = Path(os.environ.get("MEMORY_ROOT", os.path.expanduser("~/Desktop/Projects/MEMORY")))
MEMORY_DIR = MEMORY_ROOT / "memory"
MODULES_DIR = MEMORY_DIR / "modules"
BANK_DIR = MEMORY_DIR / "memory-bank"
VECTOR_DB_DIR = MEMORY_DIR / "vector_db"
SESSION_DIR = MEMORY_DIR / ".sessions"
HANDOFF_FILE = MEMORY_ROOT / ".agent-progress.md"

SESSION_DIR.mkdir(parents=True, exist_ok=True)

os.environ.setdefault("FASTMCP_LOG_LEVEL", "INFO")

from fastmcp import FastMCP

server = FastMCP("memory-server")

# ---------------------------------------------------------------------------
# Helper: ChromaDB client (lazy init)
# ---------------------------------------------------------------------------
_chroma = None

def _get_chroma():
    global _chroma
    if _chroma is None:
        try:
            import chromadb
            _chroma = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
        except Exception:
            _chroma = None
    return _chroma

def _read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

def _list_markdown_files(dirpath: Path) -> list[dict]:
    files = []
    if not dirpath.exists():
        return files
    for p in sorted(dirpath.glob("*.md")):
        files.append({"name": p.stem, "path": str(p.relative_to(MEMORY_ROOT)), "size": p.stat().st_size})
    return files

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@server.tool()
def recall_context(query: str, top_k: int = 5) -> str:
    """Return relevant memory chunks for a query. Auto-called on session start."""
    chunks = []
    chroma = _get_chroma()
    if chroma:
        try:
            collections = chroma.list_collections()
            for col in collections:
                results = col.query(query_texts=[query], n_results=top_k)
                if results and results.get("documents"):
                    for i, doc in enumerate(results["documents"][0]):
                        meta = (results.get("metadatas") or [{}])[0][i] if results.get("metadatas") else {}
                        source = meta.get("source", "unknown")
                        chunks.append(f"[source: {source}]\n{doc[:2000]}")
        except Exception as e:
            chunks.append(f"[vector search unavailable: {e}]")

    if not chunks:
        handoff = _read_file_safe(HANDOFF_FILE)
        if handoff:
            chunks.append(f"[handoff file]\n{handoff[:3000]}")

    return "\n\n---\n\n".join(chunks[:top_k]) if chunks else "No relevant memory found."


@server.tool()
def save_memory(content: str, category: str = "general", tags: list[str] = None) -> str:
    """Save a piece of knowledge to the memory bank. Persisted as markdown + vector indexed."""
    tags = tags or []
    timestamp = datetime.now().isoformat()
    slug = uuid.uuid4().hex[:8]
    entry = f"""---
created: {timestamp}
category: {category}
tags: {json.dumps(tags)}
---

{content}
"""
    filepath = BANK_DIR / f"entry-{slug}.md"
    filepath.write_text(entry)

    chroma = _get_chroma()
    if chroma:
        try:
            cols = chroma.list_collections()
            col = cols[0] if cols else chroma.create_collection("memory-modules")
            col.add(
                documents=[content],
                metadatas=[{"source": f"memory-bank/entry-{slug}.md", "category": category, "tags": ",".join(tags)}],
                ids=[f"entry-{slug}"]
            )
        except Exception:
            pass

    return f"saved as memory-bank/entry-{slug}.md"


@server.tool()
def search_memory(query: str, top_k: int = 5) -> str:
    """Semantic search across all memory modules, bank, and vector DB."""
    results = []

    chroma = _get_chroma()
    if chroma:
        try:
            collections = chroma.list_collections()
            for col in collections:
                res = col.query(query_texts=[query], n_results=top_k)
                if res and res.get("documents"):
                    for i, docs in enumerate(res["documents"]):
                        for j, doc in enumerate(docs):
                            meta = (res.get("metadatas") or [{}])[i][j] if res.get("metadatas") else {}
                            source = meta.get("source", "unknown")
                            results.append(f"[{source}]\n{doc[:2000]}")
        except Exception as e:
            results.append(f"[vector search error: {e}]")

    if not results:
        for mod in MODULES_DIR.glob("*.md"):
            text = _read_file_safe(mod)
            if query.lower() in text.lower():
                results.append(f"[{mod.name}]\n{text[:2000]}")
                if len(results) >= top_k:
                    break

    return "\n\n---\n\n".join(results[:top_k]) if results else "No results."


@server.tool()
def session_status() -> str:
    """Return current session handoff state and recent progress."""
    handoff = _read_file_safe(HANDOFF_FILE)
    progress = _read_file_safe(BANK_DIR / "progress.md")
    summary = handoff[:3000] if handoff else ""
    if progress:
        lines = progress.strip().split("\n")
        recent = [l for l in lines if "|" in l and "2026" in l][-5:]
        summary += "\n\n## Recent Sessions\n" + "\n".join(recent)
    return summary or "No session data found."


@server.tool()
def memory_stats() -> str:
    """Overview of what's stored in the memory system."""
    modules = _list_markdown_files(MODULES_DIR)
    bank = _list_markdown_files(BANK_DIR)
    sessions = _list_markdown_files(SESSION_DIR) if SESSION_DIR.exists() else []

    chroma = _get_chroma()
    vec_stats = {}
    if chroma:
        try:
            for col in chroma.list_collections():
                vec_stats[col.name] = col.count()
        except Exception:
            pass

    return json.dumps({
        "modules": {"count": len(modules), "files": [m["name"] for m in modules]},
        "memory_bank": {"count": len(bank), "files": [b["name"] for b in bank]},
        "sessions": len(sessions),
        "vector_collections": vec_stats,
        "handoff_file": HANDOFF_FILE.exists(),
        "last_updated": datetime.now().isoformat(),
    }, indent=2)


@server.tool()
def session_snapshot() -> str:
    """Save a snapshot of current session context for later resume."""
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "handoff": _read_file_safe(HANDOFF_FILE)[:5000],
    }
    slug = uuid.uuid4().hex[:12]
    path = SESSION_DIR / f"snapshot-{slug}.json"
    path.write_text(json.dumps(snapshot, indent=2))
    return f"snapshot saved: .sessions/snapshot-{slug}.json"


@server.tool()
def get_memory_modules(name_filter: str = "") -> str:
    """List or read memory modules by name pattern (e.g. '01-core', 'ml-engineering')."""
    if name_filter:
        for p in MODULES_DIR.glob(f"*{name_filter}*"):
            return _read_file_safe(p)
        return f"No module matching '{name_filter}'. Available: {', '.join(p.stem for p in sorted(MODULES_DIR.glob('*.md')))}"
    modules = _list_markdown_files(MODULES_DIR)
    return "\n".join(f"{m['name']} ({m['size']}B)" for m in modules)


if __name__ == "__main__":
    server.run(transport="sse", host="127.0.0.1", port=8932)
