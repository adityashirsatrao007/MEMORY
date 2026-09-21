# Copyright (c) 2026 Aditya Shirsatrao
# MIT License — see LICENSE file.

import os
import chromadb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import time

app = FastAPI(title="MEMORY Dashboard")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8083", "http://127.0.0.1:8083"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VECTOR_DB_PATH = os.path.expanduser("~/Desktop/Projects/MEMORY/memory/vector_db")
PROGRESS_FILE = os.path.expanduser("~/Desktop/Projects/MEMORY/memory/memory-bank/progress.md")

FREELLMAPI_URL = os.environ.get("FREELLMAPI_BASE_URL", "http://localhost:3001/v1")
FREELLMAPI_KEY = os.environ.get("FREELLMAPI_KEY")

try:
    chroma_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    collection = chroma_client.get_or_create_collection(name="antigravity_memory")
except Exception as e:
    print(f"Error connecting to ChromaDB: {e}")
    collection = None

@app.get("/")
def read_root():
    return {"status": "ok", "app": "Antigravity Supermemory Dashboard", "endpoints": ["/api/recent", "/api/stats", "/api/search?q=", "/api/save", "/api/ask"]}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/ready")
def ready():
    ok = collection is not None
    return {"status": "ready" if ok else "not ready", "db": ok}

@app.get("/api/recent")
def get_recent_memories():
    """Returns the most recent memories from the DB."""
    if not collection:
        return {"error": "Database not initialized", "memories": []}
    
    try:
        results = collection.get()
        memories = []
        
        combined = list(zip(results['ids'], results['documents'], results['metadatas']))
        combined.sort(key=lambda x: x[0], reverse=True)
        
        # Return top 20
        for id_str, doc, meta in combined[:20]:
            memories.append({
                "content": doc,
                "date": meta.get("date", ""),
                "time": meta.get("time", "")
            })
            
        return {"memories": memories}
    except Exception as e:
        return {"error": str(e), "memories": []}

@app.get("/api/stats")
def get_stats():
    """Returns stats about the vector DB."""
    if not collection:
        return {"count": 0}
    try:
        count = collection.count()
        return {"count": count}
    except Exception as e:
        return {"count": 0, "error": str(e)}

@app.get("/api/search")
def search_memories(q: str):
    """Semantic search."""
    if not collection:
        return {"error": "Database not initialized", "memories": []}
    
    if not q:
        return {"memories": []}
        
    try:
        results = collection.query(
            query_texts=[q],
            n_results=5
        )
        
        memories = []
        if results and results['documents'] and results['documents'][0]:
            for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
                memories.append({
                    "content": doc,
                    "date": meta.get("date", ""),
                    "time": meta.get("time", ""),
                    "distance": dist
                })
                
        return {"memories": memories}
    except Exception as e:
        return {"error": str(e), "memories": []}
class SaveRequest(BaseModel):
    text: str

@app.post("/api/save")
def save_memory(req: SaveRequest):
    if not collection:
        return {"error": "Database not initialized"}
    
    if not req.text:
        return {"error": "Must provide text"}
        
    try:
        ts = str(int(time.time() * 1000))
        date_str = time.strftime('%Y-%m-%d')
        time_str = time.strftime('%H:%M:%S')
        
        collection.add(
            documents=[req.text],
            metadatas=[{"date": date_str, "time": time_str, "source": "api"}],
            ids=[ts]
        )
        return {"status": "success", "id": ts}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("MEMORY_DASHBOARD_PORT", "8083"))
    print(f"Starting Dashboard on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
