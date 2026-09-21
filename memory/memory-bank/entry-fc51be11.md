---
created: 2026-08-17T13:22:48.021016
category: project-research
tags: ["deepfake", "final-year-project", "voice-clone", "forensics", "research-gaps", "parakh"]
---

Research gaps for final-year project "Parakh" (vernacular, evidence-first deepfake/voice-clone verification platform for scam victims): G1 no Hindi/Marathi voice-clone dataset under WhatsApp/telephony degradation; G2 no consumer detection for 0.5-5s compressed phone-channel Indic clips; G3 no Indic voice-clone source attribution (which TTS); G4 no explainable evidence + plain-language verdict for non-experts, FIR-ready tamper-evident report; G5 no consumer-facing flow (all commercial tools = enterprise B2B). Key 2026 evidence: "The Deepfakes We Missed" (arXiv:2605.12075) - real harms are voice-clone fraud not celebrity face-swap; 45-50% AUC benchmark->deployment collapse (2607.13234); IC3 2025 $741M AI-related losses, $352M from 60+; India 83% of AI voice scam victims lost money, 48% >Rs50k. Build on: Indic-CodecFake, SEA-Spoof, LRLspoof, ML-ITW, HAV-DF datasets; S-MGAA short-input (2601.19573); LAVA attribution (2508.02521); WavLM/AASIST detectors. Stack: Next.js + FastAPI + Celery/Kafka + PyTorch WavLM/AASIST + RAG copilot + PostgreSQL/Redis + Docker/CI.
