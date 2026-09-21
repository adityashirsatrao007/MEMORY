# AI Provider API Matrix — Aditya's Global Keys

> Master inventory of AI/ML API providers vs. what's in `~/.config/global-apikeys/keys.env`.
> Use `~/Desktop/Projects/MEMORY/add_key.sh KEY_NAME "value"` to add each missing key.
> After adding, keys load via `source ~/.config/global-apikeys/load_keys.sh`.
> Keep this file synced: source of truth = MEMORY repo, tested keys = API_TEST_REPORT.md.

Last updated: 2026-08-10

## 🔴 KEY SWEEP 2026-08-10 (re-tested all) — DEAD, regenerate when convenient
| Var | Status | Regenerate at |
|-----|--------|---------------|
| GEMINI_API_KEY | ✅ regenerated | https://aistudio.google.com/apikey |
| HF_TOKEN | ✅ regenerated | https://huggingface.co/settings/tokens |
| KIMI_API_KEY | ❌ 401 (user skipped) | https://platform.moonshot.cn |
| RESEND_API_KEY | ✅ regenerated | https://resend.com/api-keys |
| CODESTRAL_API_KEY | ~404 (Retired → use MISTRAL_API_KEY) | — |
| WANDB_API_KEY | ~404 (endpoint changed; verify dashboard) | https://wandb.ai/settings |

All others verified ✅ working (GROQ, MISTRAL, COHERE, CEREBRAS, OPENROUTER, DEEPSEEK, FIREWORKS, Zai, ROBOFLOW, FIRECRAWL, GITHUB, NVIDIA, OPENAI, SAMBANOVA, HYPERBOLIC, TAVILY, VOYAGE, JINA, ELEVENLABS, DEEPGRAM, ASSEMBLYAI, EXA, PINECONE, QDRANT(JWT), SARVAM, XAI(no credits), ANTHROPIC(no credits)).

## 🆓 FREE MODELS AVAILABLE ON YOUR OWNED KEYS
- **OpenRouter `:free` — 14 models** (gemma-4-26b/31b, nemotron-3 navio/ultra, gpt-oss-20b, poolside laguna s/xs, ling-3.0-tiny, cohere north-mini-code, ...). 50 req/day by default; $10 credit raises to 1,000 req/model/day.
- **Groq free tier** (Llama/Gemma/Whisper) — verify current quotas at console.groq.com.
- **Gemini free tier + TTS on existing key**: `gemini-3.1-flash-tts-preview` (no new key — regenerate GEMINI key first).
- **SambaNova** — free tier w/ GitHub login (DeepSeek-V3/Llama endpoints).
- **Hyperbolic** — recurring weekly free credits (5 serverless models incl. DeepSeek-V3/R1).
- **Z.ai** — GLM-4-Flash class free models on ZAI_API_KEY.

## 💎 NEW FREE PROVIDERS TO SIGN UP (2026 researched)
| Provider | Free tier | Signup | Key var |
|----------|-----------|--------|---------|
| **Cloudflare Workers AI** | 10,000 neurons/day FREE | https://dash.cloudflare.com → Workers AI | CLOUDFLARE_API_KEY (have!) + CLOUDFLARE_ACCOUNT_ID (have!) |
| **OVHcloud AI Endpoints** | anonymous no-key tier / free credits | https://endpoints.ai.cloud.ovh.net | OVHAI_API_KEY (optional) |
| **SiliconFlow** | free Qwen + BGE embeddings | https://siliconflow.com | SILICONFLOW_API_KEY (was paid-list; move to free) |
| **GitHub Models** | RETIRED Jul 30 2026 → Microsoft Foundry | https://github.com/marketplace/models | reuse GITHUB_TOKEN |
| **NVIDIA build.nvidia.com** | free in-browser NIM endpoints | https://build.nvidia.com | reuse NVIDIA_NIM_API_KEY |

## ✔ Already Have (30 AI-related vars in keys.env)

| Var | Provider |
|-----|----------|
| OPENROUTER_API_KEY | OpenRouter (aggregator) |
| GEMINI_API_KEY / GOOGLE_API_KEY | Google Gemini |
| MISTRAL_API_KEY / CODESTRAL_API_KEY | Mistral AI |
| DEEPSEEK_API_KEY | DeepSeek |
| GROQ_API_KEY | Groq |
| COHERE_API_KEY | Cohere |
| CEREBRAS_API_KEY | Cerebras |
| FIREWORKS_API_KEY | Fireworks AI |
| NVIDIA_NIM_API_KEY | NVIDIA NIM |
| KIMI_API_KEY | Moonshot (Kimi) |
| ZAI_API_KEY | Z.ai (Zhipu GLM) |
| HF_TOKEN / HUGGINGFACE_API_KEY | Hugging Face |
| SARVAM_API_KEY | Sarvam AI (Indian languages) |
| ROBOFLOW_API_KEY | Roboflow (vision) |
| WANDB_API_KEY | Weights & Biases |
| KAGGLE_ACCESS_TOKEN | Kaggle |
| FIRECRAWL_API_KEY | Firecrawl (web/scrape) |
| FREELLMAPI_KEY | freellmapi (aggregator) |
| OPENCODE_API_KEY | opencode |
| GLIF_API_TOKEN | Glif |
| CLAY_API_KEY | Clay |
| WAFER_API_KEY | Wafer |
| KALCEND_API_KEY | Kalcend |
| GITHUB_TOKEN / GITHUB_API_KEY | GitHub (incl. GitHub Models) |

## ❌ Missing — Recommended to Add  (skip-paid: TOGETHER, MINIMAX, DASHSCOPE, PERPLEXITY, AI21 = paid; user preference: FREE only)

### LLM / Chat / Frontier
| Recommended var | Provider | Get key at |
|-----------------|----------|------------|
| OPENAI_API_KEY | OpenAI GPT | https://platform.openai.com/api-keys |
| ANTHROPIC_API_KEY | Anthropic Claude | https://console.anthropic.com/settings/keys |
| XAI_API_KEY | xAI Grok | https://console.x.ai |
| TOGETHER_API_KEY | Together AI | https://api.together.ai/settings/api-keys |
| SAMBANOVA_API_KEY | SambaNova | https://cloud.sambanova.ai/apis |
| PERPLEXITY_API_KEY | Perplexity (Sonar) | https://www.perplexity.ai/settings/api |
| MINIMAX_API_KEY | MiniMax | https://platform.minimax.io/api-key |
| DASHSCOPE_API_KEY | Alibaba Qwen | https://dashscope.intl.aliyuncs.com |
| AI21_API_KEY | AI21 Jamba | https://studio.ai21.com/account/api-key |
| HYPERBOLIC_API_KEY | Hyperbolic (FREE, weekly credits) | https://hyperbolic.xyz |
| DEEPINFRA_API_KEY | DeepInfra | https://deepinfra.com/dash/api_keys |
| SILICONFLOW_API_KEY | SiliconFlow | https://siliconflow.com/account/ak |
| NOVITA_API_KEY | Novita AI | https://novita.ai/setting/key |
| AIMLAPI_API_KEY | AI/ML API | https://aimlapi.com/keys |

### Speech — STT / TTS (voice agents, threat-intel audio)
| Recommended var | Provider | Get key at |
|-----------------|----------|------------|
| ELEVENLABS_API_KEY ✅ | ElevenLabs | https://elevenlabs.io/app/settings/api-keys |
| DEEPGRAM_API_KEY | Deepgram | https://console.deepgram.com |
| ASSEMBLYAI_API_KEY | AssemblyAI | https://www.assemblyai.com/app/account |
| CARTESIA_API_KEY | Cartesia (sub-90ms TTS) | https://cartesia.ai/keys |
| HUME_API_KEY | Hume AI (emotion TTS) | https://hume.ai/dashboard/settings |

### Embeddings / RAG
| Recommended var | Provider | Get key at |
|-----------------|----------|------------|
| JINA_API_KEY | Jina AI (FREE starter bundle) | https://jina.ai/api-dashboard |
| VOYAGE_API_KEY | Voyage AI (FREE 200M one-time) | https://dash.voyageai.com/api-keys |
| UPSTAGE_API_KEY | Upstage (Solar) | https://console.upstage.ai/api-keys |

### Image / Video / Multimodal
| Recommended var | Provider | Get key at |
|-----------------|----------|------------|
| STABILITY_API_KEY | Stability AI | https://platform.stability.ai/account/keys |
| REPLICATE_API_TOKEN | Replicate | https://replicate.com/account/api-tokens |
| BFL_API_KEY | Black Forest Labs (Flux) | https://api.bfl.ai |

### Search / Agent grounding
| Recommended var | Provider | Get key at |
|-----------------|----------|------------|
| TAVILY_API_KEY | Tavily (FREE 1k/mo) | https://app.tavily.com |
| EXA_API_KEY | Exa (web search) | https://dashboard.exa.ai/api-keys |
| BRAVE_API_KEY | Brave Search (paid) | https://brave.com/search/api |

### Vector DBs (RAG infra)
| Recommended var | Provider | Get key at |
|-----------------|----------|------------|
| PINECONE_API_KEY | Pinecone | https://app.pinecone.io |
| QDRANT_API_KEY | Qdrant Cloud | https://cloud.qdrant.io |

## 🎁 Note
- **GitHub Models** (free GPT/Claude/Grok/Llama in browser) — reuse existing `GITHUB_TOKEN`.
- **NVIDIA Build** (free in-browser NIM) — reuse existing `NVIDIA_NIM_API_KEY`.
- **Azure OpenAI / AWS Bedrock / Vertex AI** — not single keys; need portal/service-account creds; add `AZURE_OPENAI_API_KEY`/`AWS_*` only when a project needs them.