# Advanced Semantic Search

Premium module — requires Pro or Enterprise license.

## Features
- Multi-query fusion (run N queries, merge results by relevance)
- Hybrid search: vector (ChromaDB) + keyword (BM25) in one pass
- Cross-lingual retrieval: query in English, find results in any language
- Custom reranking with configurable scoring weights

## Setup
```bash
memory premium install advanced-search
```

Then configure in `~/.config/memory/config.toml`:
```toml
[search]
engine = "advanced"
fusion_queries = 3
hybrid_weight = 0.7
```
