#!/usr/bin/env bash
# MEMORY — Start all infrastructure services
set -euo pipefail

MEMORY_ROOT="${MEMORY_ROOT:-$HOME/Desktop/Projects/MEMORY}"
source "$MEMORY_ROOT/.venv/bin/activate" 2>/dev/null

echo "=== Starting MEMORY Infrastructure ==="

# 1. Vector DB API (port 8082)
echo "Starting vector DB API on :8082..."
cd "$MEMORY_ROOT"
python3 -c "
import chromadb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, os, json

app = FastAPI(title='MEMORY Vector DB')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:8082', 'http://127.0.0.1:8082', 'http://localhost:8083', 'http://127.0.0.1:8083'], allow_methods=['*'], allow_headers=['*'])

DB = os.path.join('$MEMORY_ROOT', 'memory', 'vector_db')
client = chromadb.PersistentClient(path=DB)
col = client.get_or_create_collection('antigravity_memory')

@app.get('/api/search')
def search(q: str = '', top_k: int = 5):
    if not q:
        results = col.get()
        seen = []
        for m in results['metadatas']:
            f, s = m.get('file','?'), m.get('section','?')
            if {'file':f,'section':s} not in seen:
                seen.append({'file':f,'section':s})
        return {'memories': seen}
    results = col.query(query_texts=[q], n_results=top_k)
    memories = []
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        memories.append({'content': doc[:500], 'source': meta.get('file','?'), 'section': meta.get('section','?'), 'distance': dist})
    return {'memories': memories}

@app.get('/api/stats')
def stats():
    return {'total_chunks': col.count(), 'collection': 'antigravity_memory'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8082)
" &
VECTOR_PID=$!
echo "  Vector DB API PID: $VECTOR_PID"

# 2. Dashboard (port 8083)
echo "Starting dashboard on :8083..."
python3 "$MEMORY_ROOT/tools/dashboard.py" &
DASHBOARD_PID=$!
echo "  Dashboard PID: $DASHBOARD_PID"

echo ""
echo "=== Services Running ==="
echo "  Vector DB API: http://localhost:8082"
echo "  Dashboard:     http://localhost:8083"
echo ""
echo "  To stop: kill $VECTOR_PID $DASHBOARD_PID"
echo ""

wait
