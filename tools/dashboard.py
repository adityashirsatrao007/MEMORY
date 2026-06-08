import os
from fastapi import FastAPI
import chromadb

app = FastAPI(title="Antigravity Supermemory Dashboard")

VECTOR_DB_PATH = os.path.expanduser("~/Desktop/Projects/MEMORY/memory/vector_db")
PROGRESS_FILE = os.path.expanduser("~/Desktop/Projects/MEMORY/memory/memory-bank/progress.md")

try:
    chroma_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    collection = chroma_client.get_or_create_collection(name="antigravity_memory")
except Exception as e:
    print(f"Error connecting to ChromaDB: {e}")
    collection = None

@app.get("/")
def read_root():
    return {"status": "ok", "app": "Antigravity Supermemory Dashboard", "endpoints": ["/api/recent", "/api/stats", "/api/search?q=", "/api/save", "/api/ask"]}

@app.get("/api/recent")
def get_recent_memories():
    """Returns the most recent memories from the DB."""
    if not collection:
        return {"error": "Database not initialized", "memories": []}
    
    try:
        # We can query all documents (or a subset) by fetching
        results = collection.get()
        memories = []
        
        # Sort by timestamp (id) descending
        combined = list(zip(results['ids'], results['documents'], results['metadatas']))
        combined.sort(key=lambda x: int(x[0]), reverse=True)
        
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
            n_results=10
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

from pydantic import BaseModel
from typing import Optional
import urllib.request
from bs4 import BeautifulSoup
import markdownify
import time
import google.generativeai as genai

class SaveRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

@app.post("/api/save")
def save_memory(req: SaveRequest):
    if not collection:
        return {"error": "Database not initialized"}
    
    content_to_save = ""
    
    if req.url:
        try:
            req_obj = urllib.request.Request(req.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_obj) as response:
                html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            # Extract main content (simplified)
            text_content = markdownify.markdownify(str(soup), heading_style="ATX")
            content_to_save = f"Saved URL: {req.url}\n\n{text_content}"
        except Exception as e:
            return {"error": f"Failed to fetch URL: {e}"}
    elif req.text:
        content_to_save = req.text
    else:
        return {"error": "Must provide text or url"}
        
    try:
        ts = str(int(time.time() * 1000))
        date_str = time.strftime('%Y-%m-%d')
        time_str = time.strftime('%H:%M:%S')
        
        collection.add(
            documents=[content_to_save],
            metadatas=[{"date": date_str, "time": time_str, "source": "api"}],
            ids=[ts]
        )
        return {"status": "success", "id": ts}
    except Exception as e:
        return {"error": str(e)}

class AskRequest(BaseModel):
    query: str

@app.post("/api/ask")
def ask_ai(req: AskRequest):
    if not collection:
        return {"error": "Database not initialized"}
        
    try:
        results = collection.query(
            query_texts=[req.query],
            n_results=5
        )
        
        context = ""
        if results and results['documents'] and results['documents'][0]:
            for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                context += f"- [{meta.get('date')} {meta.get('time')}] {doc}\n\n"
                
        # Use Gemini to synthesize
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return {"answer": "Error: GEMINI_API_KEY not found in environment.", "context": context}
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"You are Antigravity Supermemory AI. Answer the user's query based ONLY on the following memory context.\n\nContext:\n{context}\n\nQuery: {req.query}\nAnswer:"
        
        response = model.generate_content(prompt)
        return {"answer": response.text, "context_used": len(results['documents'][0])}
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("MEMORY_DASHBOARD_PORT", "8083"))
    print(f"Starting Dashboard on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
