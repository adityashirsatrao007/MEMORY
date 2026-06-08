import chromadb
import os

VECTOR_DB_PATH = os.path.expanduser("~/Desktop/Projects/MEMORY/memory/vector_db")
GEMINI_PATH = os.path.expanduser("~/Desktop/Projects/MEMORY/GEMINI.md")

client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
collection = client.get_or_create_collection(name="antigravity_memory")

with open(GEMINI_PATH) as f:
    lines = f.readlines()

chunks = []
current_section = ""
current_chunk = []
line_start = 1

for i, line in enumerate(lines, 1):
    if line.startswith("## "):
        if current_chunk:
            chunks.append((current_section, "".join(current_chunk), line_start, i - 1))
        current_section = line.strip("# \n")
        current_chunk = [line]
        line_start = i
    else:
        current_chunk.append(line)

if current_chunk:
    chunks.append((current_section, "".join(current_chunk), line_start, len(lines)))

existing = collection.get()
if existing and existing["ids"]:
    print(f"Vector DB already has {len(existing['ids'])} entries. Skipping seed.")
else:
    ids = []
    documents = []
    metadatas = []
    for i, (section, text, start, end) in enumerate(chunks):
        if len(text.strip()) < 20:
            continue
        ids.append(f"gemini-section-{i:04d}")
        documents.append(text)
        metadatas.append({"source": "GEMINI.md", "section": section, "lines": f"{start}-{end}"})
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Seeded {len(ids)} sections from GEMINI.md into vector DB")
    print(f"Dashboard available at http://localhost:8082")
    print(f"Try: curl http://localhost:8082/api/search?q=zero+token+cli")
