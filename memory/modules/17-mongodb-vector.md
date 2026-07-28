# MongoDB Atlas as Vector DB

## When to Use
- Chunks > 10,000 (ChromaDB slows down)
- Multi-device sync needed
- Production deployments
- Need full-text + vector hybrid search

## Setup
```bash
# Install MongoDB Atlas free tier
# https://cloud.mongodb.com → Create free M0 cluster

# Save connection string
echo "MONGODB_URI=mongodb+srv://<user>:<pass>@cluster0.xxxxx.mongodb.net" >> ~/.config/global-apikeys/keys.env

# Install driver
uv pip install pymongo sentence-transformers
```

## Integration with MEMORY
```python
import os
import pymongo
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

client = pymongo.MongoClient(os.environ['MONGODB_URI'])
db = client.memory
col = db.vectors

# Create vector search index (run once)
col.create_search_index(
    name="vector_index",
    definition={
        "fields": [{
            "type": "vector",
            "path": "embedding",
            "numDimensions": 384,
            "similarity": "cosine"
        }]
    }
)

# Seed
for chunk in chunks:
    embedding = model.encode(chunk['text']).tolist()
    col.insert_one({
        'text': chunk['text'],
        'embedding': embedding,
        'source': chunk['source'],
        'section': chunk['section']
    })

# Search
query_embedding = model.encode("authentication security").tolist()
results = col.aggregate([
    {"$vectorSearch": {
        "index": "vector_index",
        "path": "embedding",
        "queryVector": query_embedding,
        "numCandidates": 100,
        "limit": 5
    }}
])
for doc in results:
    print(f"[{doc['source']}] {doc['section']}: {doc['text'][:100]}")
```

## Migration from ChromaDB
```python
# Read from ChromaDB
import chromadb
c = chromadb.PersistentClient(path='memory/vector_db')
col = c.get_or_create_collection('antigravity_memory')
all_data = col.get()

# Write to MongoDB
for doc, meta, id_ in zip(all_data['documents'], all_data['metadatas'], all_data['ids']):
    embedding = model.encode(doc).tolist()
    mongo_col.insert_one({
        'text': doc,
        'embedding': embedding,
        'source': meta.get('file', ''),
        'section': meta.get('section', ''),
        'chunk_id': id_
    })
```

## MongoDB Student Benefits
- $50 Atlas credit (free tier M0 forever)
- Free MongoDB Compass (GUI)
- Free certification ($150 value)
- University courses free
