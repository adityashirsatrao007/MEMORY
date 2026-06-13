# API Reference

## ChromaDB Vector Search

### Search Modules
```bash
curl -s "localhost:8082/api/search?q=your+topic" | jq -r '.memories[0].content // empty'
```

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `q` | string | Search query (required) |
| `top_k` | int | Results to return (default: 3) |

**Response:**
```json
{
  "memories": [
    {
      "content": "Relevant chunk text...",
      "metadata": {
        "module": "01-core-rules",
        "line": 42
      },
      "score": 0.89
    }
  ]
}
```

## freellmapi (0-Cost LLM Proxy)

### Chat Completion (OpenAI-compatible)
```bash
curl http://localhost:3001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FREELLMAPI_KEY" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**Models:**
| Model | Routes To |
|-------|-----------|
| `auto` | Auto-select across 16 providers |
| `gemini-2.5-flash` | Google Gemini (free tier) |
| `claude-sonnet-4` | Anthropic (via OpenRouter) |
| `deepseek-v4` | DeepSeek |

### Health Check
```bash
curl http://localhost:3001/health
# → {"status":"ok","providers_available":12}
```

## Enola (Architecture Snapshot)

### Generate Snapshot
```bash
enola generate_snapshot .
```

### Explore Module
```bash
enola explore <module_name>
```

### Impact Analysis
```bash
enola impact_analysis <target>
```

## CodeBurn (Token Observability)

### Status
```bash
codeburn status
```

### Optimize
```bash
codeburn optimize
```

### Log Event
```bash
codeburn log --type system "message"
```

## Memory Search (Vector DB via CLI)

```bash
memory-search "<query>" [top_k=3]
```

Returns the most relevant chunks from ChromaDB with source module references. Use this before loading any module to save tokens.

## Dashboard

| URL | Service |
|-----|---------|
| `http://localhost:8082/admin` | FCC Admin UI |
| `http://localhost:5173` | freellmapi dashboard |
| `http://localhost:8083` | MEMORY dashboard (alt) |
