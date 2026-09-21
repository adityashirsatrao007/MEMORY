# API Key Routing — Use-Case → Best Key (free-first)

> ⚠️ **Directive from Aditya: he will NOT command explicitly which key/provider to use.**
> Whenever a task needs any model API (LLM, embeddings, speech, search, scraping, storage), **proactively pick the right provider from this matrix yourself** and just use it — do not ask which key, do not wait for instructions. Free-first, quality-aware, per the table below.

> Decides which provider to call for a task using Aditya's global keys (`source ~/.config/global-apikeys/load_keys.sh`).
> Priority: FREE tier first -> owned paid (OpenAI/Anthropic/xAI) only when quality requires -> local/free proxies (freellmapi).
> All keys verified 2026-08-10 (see AI_PROVIDERS.md for regen links).

## LLM / Chat / Reasoning
| Use case | Provider | Key | Base URL |
|----------|----------|-----|----------|
| General chat, vision, 1M ctx, FREE | Gemini Flash | `GEMINI_API_KEY` | `https://generativelanguage.googleapis.com` |
| Speed leader (Llama/Gemma/Whisper) | Groq | `GROQ_API_KEY` | `https://api.groq.com/openai/v1` |
| Free frontier-ish (14 `:free`) | OpenRouter | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` |
| Cheap strong coding/reasoning | DeepSeek | `DEEPSEEK_API_KEY` | `https://api.deepseek.com/v1` |
| Code gen (Codestral) / EU | Mistral | `MISTRAL_API_KEY` | `https://api.mistral.ai/v1` |
| Free weekly credits (DeepSeek/R1) | Hyperbolic | `HYPERBOLIC_API_KEY` | `https://api.hyperbolic.xyz/v1` |
| Free fast DeepSeek/Llama (GitHub login) | SambaNova | `SAMBANOVA_API_KEY` | `https://api.sambanova.ai/v1` |
| GLM Flash free | Z.ai | `ZAI_API_KEY` | `https://api.z.ai/api/paas/v4` |
| Ultra-fast serving (best-effort) | Cerebras | `CEREBRAS_API_KEY` | `https://api.cerebras.ai/v1` |
| Nemotron free / content safety | NVIDIA NIM | `NVIDIA_NIM_API_KEY` | `https://integrate.api.nvidia.com/v1` |
| 10k FREE neurons/day (serverless) | Cloudflare Workers AI | `CLOUDFLARE_TOKEN` | `https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT/ai/run` |

**Reserved (have but billable / no credits):** OpenAI `OPENAI_API_KEY` (pay), Anthropic `ANTHROPIC_API_KEY` (0 balance), xAI `XAI_API_KEY` (0 balance). Prefer OpenRouter route for these if the model exists there.

## Embeddings & RAG
| Use case | Provider | Key |
|----------|----------|-----|
| Highest retrieval quality (200M free) | **Voyage** | `VOYAGE_API_KEY` |
| Long-doc / multilingual / multimodal | **Jina v3** | `JINA_API_KEY` |
| True omni-modal (text/image/video/audio) | **Gemini** embedding | `GEMINI_API_KEY` |
| Embed + Rerank single vendor, 100+ langs | **Cohere** | `COHERE_API_KEY` |
| Rerank (with embedding pipeline) | **Jina/Cohere Rerank** | `JINA_API_KEY` / `COHERE_API_KEY` |

## Vector DBs
| Tier | Store | Env vars |
|------|-------|----------|
| Free 1GB cloud | **Qdrant** (JWT) | `QDRANT_API_KEY`, `QDRANT_URL` |
| Free-tier cloud | **Pinecone** | `PINECONE_API_KEY` (+ per-index host) |
| Local/offscreen | **Chroma** (seeded from MEMORY modules) | none |

## Speech
| Use case | Provider | Key |
|----------|----------|-----|
| Real-time STT, low latency | **Deepgram** (Nova-3) | `DEEPGRAM_API_KEY` |
| STT + audio intelligence (sentiment/PII/docs) | **AssemblyAI** | `ASSEMBLYAI_API_KEY` |
| Best TTS quality + cloning (10k free chars/mo) | **ElevenLabs** | `ELEVENLABS_API_KEY` |
| FREE TTS via Gemini | Gemini TTS preview | `GEMINI_API_KEY` |
| Indian-language STT/TTS/translation | **Sarvam** | `SARVAM_API_KEY` |
| Whisper (fast/free tier) | Groq | `GROQ_API_KEY` |

## Search / Agent grounding / Scraping
| Use case | Provider | Key |
|----------|----------|-----|
| Pure web search, docs/sources (1k/mo free) | **Tavily** | `TAVILY_API_KEY` |
| Neural/answer-grounded search | **Exa** | `EXA_API_KEY` |
| Scrape/crawl/map/extract + search | **Firecrawl** | `FIRECRAWL_API_KEY` |
| Wikipedia-style results, citations | Perplexity (paid) | `PERPLEXITY_API_KEY` (not yet) |

## Vision / Image / OCR
| Use case | Provider | Key |
|----------|----------|-----|
| Vision/OCR/images (multimodal FREE) | **Gemini** | `GEMINI_API_KEY` |
| Custom trained detection | **Roboflow** | `ROBOFLOW_API_KEY` |
| OCR (EN+Hindi) offline | EasyOCR / PaddleOCR | none (local) |

## ML Ops / Data
| Use case | Tool/Provider | Key |
|----------|---------------|-----|
| Experiment tracking | **Weights & Biases** | `WANDB_API_KEY`(verify) |
| Datasets/kernels | **Kaggle** | `KAGGLE_ACCESS_TOKEN` |
| Models / inference server | **Hugging Face** | `HF_TOKEN` |
| Email delivery | **Resend** | `RESEND_API_KEY` |

## Engineering workstreams → suggested stack
- **RAG knowledge base**: Firecrawl (ingest) → Jina/Voyage (embed) → Qdrant/Pinecone (store) → Groq/Gemini (answer) + Cohere rerank.
- **SentinelX (phishing/scam, EN+IN)**: Fediverse/email gateways → Deepgram/AssemblyAI (voice) → Sarvam (translation/analysis) → Groq/Gemini (triage) → Tavily/Exa (threat lookup) → OpenRouter fallback.
- **Voice agent (<500ms)**: Deepgram Nova-3 → fast LLM (Groq Llama or Gemini Flash) → ElevenLabs Flash / Groq TTS.
- **Data pipeline orchestration**: Airflow/dbt (unchanged) + WandB for model logging, Kaggle datasets, HF for fine-tune basis.
- **Cheapest coding agent**: DeepSeek (code) via `CHAT_BASE`/`AUTH_TOKEN` pattern from Module 10 (base URL w/o `/v1`).