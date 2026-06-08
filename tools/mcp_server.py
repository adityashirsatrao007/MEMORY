import os
import chromadb
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Antigravity Supermemory Vector DB")

VECTOR_DB_PATH = os.path.expanduser("~/Desktop/Projects/MEMORY/vector_db")

# Initialize ChromaDB
try:
    chroma_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    collection = chroma_client.get_or_create_collection(name="antigravity_memory")
except Exception as e:
    print(f"Error connecting to ChromaDB: {e}")
    collection = None

@mcp.tool()
def search_antigravity_memory(query: str, limit: int = 5) -> str:
    """
    Search your local Antigravity Supermemory using Semantic Search (Vector DB).
    This will find conceptually related memories, even if exact keywords don't match.
    
    Args:
        query: The string to search for (e.g., 'email automation', 'UI bugs').
        limit: The maximum number of relevant memories to return (default: 5).
    """
    if not collection:
        return "Vector database is not initialized or unavailable."
    
    try:
        results = collection.query(
            query_texts=[query],
            n_results=limit
        )
        
        if not results or not results['documents'] or not results['documents'][0]:
            return f"No memories found semantically matching '{query}'."
            
        formatted_results = []
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]
        
        for doc, meta, dist in zip(documents, metadatas, distances):
            # dist is the distance score (lower is more relevant)
            date_str = meta.get('date', 'Unknown date')
            time_str = meta.get('time', 'Unknown time')
            formatted_results.append(f"- **[{date_str} {time_str}]** {doc} (Distance: {dist:.2f})")
            
        return "Found the following semantic matches:\n\n" + "\n".join(formatted_results)
        
    except Exception as e:
        return f"Error querying vector database: {e}"

if __name__ == "__main__":
    print("Starting Antigravity Supermemory MCP Server with ChromaDB Semantic Search...")
    mcp.run(transport='stdio')
