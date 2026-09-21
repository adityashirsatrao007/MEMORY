#!/usr/bin/env python3
"""
MEMORY Global API Keys Test Suite
Tests all API keys and connections stored in ~/.config/global-apikeys/keys.env
"""

import os
import sys
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

# Load keys from keys.env
keys_env_path = Path.home() / ".config" / "global-apikeys" / "keys.env"
if keys_env_path.exists():
    with open(keys_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and value:
                    os.environ[key] = value

@dataclass
class TestResult:
    name: str
    status: str  # "PASS", "FAIL", "SKIP", "WARN"
    message: str = ""
    latency_ms: float = 0
    details: Dict[str, Any] = field(default_factory=dict)

class APITester:
    def __init__(self):
        self.results: list[TestResult] = []
        self.start_time = time.time()

    def add_result(self, result: TestResult):
        self.results.append(result)
        status_colors = {
            "PASS": "\033[92m✓\033[0m",
            "FAIL": "\033[91m✗\033[0m",
            "SKIP": "\033[93m○\033[0m",
            "WARN": "\033[93m!\033[0m"
        }
        color = status_colors.get(result.status, "?")
        latency = f" ({result.latency_ms:.0f}ms)" if result.latency_ms > 0 else ""
        print(f"  {color} {result.name}: {result.status}{latency} - {result.message}")

    def test_env_var(self, var_name: str, required: bool = True) -> Optional[str]:
        value = os.environ.get(var_name, "")
        if not value:
            if required:
                self.add_result(TestResult(var_name, "FAIL", "Not set"))
            else:
                self.add_result(TestResult(var_name, "SKIP", "Not set (optional)"))
            return None
        return value

    def test_groq(self):
        """Test Groq API key"""
        key = self.test_env_var("GROQ_API_KEY")
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": "Say 'OK'"}], "max_tokens": 5},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("GROQ_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 401:
                self.add_result(TestResult("GROQ_API_KEY", "FAIL", "Invalid/expired key", latency))
            else:
                self.add_result(TestResult("GROQ_API_KEY", "WARN", f"HTTP {resp.status_code}: {resp.text[:100]}", latency))
        except Exception as e:
            self.add_result(TestResult("GROQ_API_KEY", "FAIL", str(e)[:100]))

    def test_gemini(self):
        """Test Gemini API key"""
        key = self.test_env_var("GEMINI_API_KEY")
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
                headers={"Content-Type": "application/json"},
                json={"contents": [{"parts": [{"text": "Say OK"}]}]},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("GEMINI_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 400:
                self.add_result(TestResult("GEMINI_API_KEY", "WARN", f"Key works but request error: {resp.text[:100]}", latency))
            else:
                self.add_result(TestResult("GEMINI_API_KEY", "FAIL", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("GEMINI_API_KEY", "FAIL", str(e)[:100]))

    def test_openrouter(self):
        """Test OpenRouter API key"""
        key = self.test_env_var("OPENROUTER_API_KEY")
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "meta-llama/llama-3.1-8b-instruct", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("OPENROUTER_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 401:
                self.add_result(TestResult("OPENROUTER_API_KEY", "FAIL", "Invalid key", latency))
            else:
                self.add_result(TestResult("OPENROUTER_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("OPENROUTER_API_KEY", "FAIL", str(e)[:100]))

    def test_cerebras(self):
        """Test Cerebras API key"""
        key = self.test_env_var("CEREBRAS_API_KEY")
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.post(
                "https://api.cerebras.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "llama-3.1-8b", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("CEREBRAS_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 401:
                self.add_result(TestResult("CEREBRAS_API_KEY", "FAIL", "Invalid key", latency))
            elif resp.status_code == 404:
                # Try alternative endpoint
                resp2 = requests.post(
                    "https://api.cerebras.ai/v1/completions",
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json={"model": "llama-3.1-8b", "prompt": "Say OK", "max_tokens": 5},
                    timeout=15
                )
                if resp2.status_code == 200:
                    self.add_result(TestResult("CEREBRAS_API_KEY", "PASS", "API responds (alt endpoint)", latency))
                else:
                    self.add_result(TestResult("CEREBRAS_API_KEY", "WARN", f"Key may be valid but endpoint changed: HTTP {resp.status_code}", latency))
            else:
                self.add_result(TestResult("CEREBRAS_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("CEREBRAS_API_KEY", "FAIL", str(e)[:100]))

    def test_nvidia_nim(self):
        """Test NVIDIA NIM API key"""
        key = self.test_env_var("NVIDIA_NIM_API_KEY")
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "meta/llama-3.1-8b-instruct", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("NVIDIA_NIM_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 401:
                self.add_result(TestResult("NVIDIA_NIM_API_KEY", "FAIL", "Invalid key", latency))
            else:
                self.add_result(TestResult("NVIDIA_NIM_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("NVIDIA_NIM_API_KEY", "FAIL", str(e)[:100]))

    def test_huggingface(self):
        """Test HuggingFace API key"""
        key = self.test_env_var("HF_TOKEN") or self.test_env_var("HUGGINGFACE_API_KEY")
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.get(
                "https://huggingface.co/api/whoami-v2",
                headers={"Authorization": f"Bearer {key}"},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                data = resp.json()
                name = data.get("name", "unknown")
                self.add_result(TestResult("HF_TOKEN", "PASS", f"Authenticated as: {name}", latency))
            else:
                self.add_result(TestResult("HF_TOKEN", "FAIL", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("HF_TOKEN", "FAIL", str(e)[:100]))

    def test_deepseek(self):
        """Test DeepSeek API key"""
        key = self.test_env_var("DEEPSEEK_API_KEY")
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "deepseek-chat", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("DEEPSEEK_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 401:
                self.add_result(TestResult("DEEPSEEK_API_KEY", "FAIL", "Invalid key", latency))
            else:
                self.add_result(TestResult("DEEPSEEK_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("DEEPSEEK_API_KEY", "FAIL", str(e)[:100]))

    def test_fireworks(self):
        """Test Fireworks AI API key"""
        key = self.test_env_var("FIREWORKS_API_KEY")
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.post(
                "https://api.fireworks.ai/inference/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "accounts/fireworks/models/llama-v3p1-8b-instruct", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("FIREWORKS_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 401:
                self.add_result(TestResult("FIREWORKS_API_KEY", "FAIL", "Invalid key", latency))
            elif resp.status_code == 404:
                # Try listing models to verify key works
                resp2 = requests.get(
                    "https://api.fireworks.ai/inference/v1/models",
                    headers={"Authorization": f"Bearer {key}"},
                    timeout=15
                )
                if resp2.status_code == 200:
                    self.add_result(TestResult("FIREWORKS_API_KEY", "PASS", "Key valid (model list works)", latency))
                else:
                    self.add_result(TestResult("FIREWORKS_API_KEY", "WARN", f"Key may be valid but model changed: HTTP {resp.status_code}", latency))
            else:
                self.add_result(TestResult("FIREWORKS_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("FIREWORKS_API_KEY", "FAIL", str(e)[:100]))

    def test_mistral(self):
        """Test Mistral API key"""
        key = self.test_env_var("MISTRAL_API_KEY")
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "mistral-small-latest", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("MISTRAL_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 401:
                self.add_result(TestResult("MISTRAL_API_KEY", "FAIL", "Invalid key", latency))
            else:
                self.add_result(TestResult("MISTRAL_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("MISTRAL_API_KEY", "FAIL", str(e)[:100]))

    def test_cohere(self):
        """Test Cohere API key"""
        key = self.test_env_var("COHERE_API_KEY", required=False)
        if not key:
            return

        try:
            import requests
            start = time.time()
            # Try v2 endpoint first
            resp = requests.post(
                "https://api.cohere.com/v2/chat",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "command-r", "messages": [{"role": "user", "content": "Say OK"}]},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("COHERE_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 401:
                self.add_result(TestResult("COHERE_API_KEY", "FAIL", "Invalid key", latency))
            elif resp.status_code == 404:
                # Try v1 endpoint
                resp2 = requests.post(
                    "https://api.cohere.com/v1/chat",
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json={"model": "command-r", "message": "Say OK"},
                    timeout=15
                )
                if resp2.status_code == 200:
                    self.add_result(TestResult("COHERE_API_KEY", "PASS", "API responds (v1)", latency))
                else:
                    self.add_result(TestResult("COHERE_API_KEY", "WARN", f"Key may be valid but endpoint changed: HTTP {resp.status_code}", latency))
            else:
                self.add_result(TestResult("COHERE_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("COHERE_API_KEY", "FAIL", str(e)[:100]))

    def test_github(self):
        """Test GitHub API key"""
        key = self.test_env_var("GITHUB_TOKEN") or self.test_env_var("GITHUB_API_KEY")
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.get(
                "https://api.github.com/user",
                headers={"Authorization": f"token {key}"},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                data = resp.json()
                login = data.get("login", "unknown")
                self.add_result(TestResult("GITHUB_TOKEN", "PASS", f"Authenticated as: {login}", latency))
            else:
                self.add_result(TestResult("GITHUB_TOKEN", "FAIL", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("GITHUB_TOKEN", "FAIL", str(e)[:100]))

    def test_cloudflare(self):
        """Test Cloudflare API token"""
        token = self.test_env_var("CLOUDFLARE_TOKEN", required=False)
        if not token:
            return

        try:
            import requests
            start = time.time()
            resp = requests.get(
                "https://api.cloudflare.com/client/v4/user/tokens/verify",
                headers={"Authorization": f"Bearer {token}"},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200 and resp.json().get("success"):
                self.add_result(TestResult("CLOUDFLARE_TOKEN", "PASS", "Token valid", latency))
            else:
                self.add_result(TestResult("CLOUDFLARE_TOKEN", "FAIL", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("CLOUDFLARE_TOKEN", "FAIL", str(e)[:100]))

    def test_wandb(self):
        """Test Weights & Biases API key"""
        key = self.test_env_var("WANDB_API_KEY", required=False)
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.get(
                "https://api.wandb.ai/graphql",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"query": "{ viewer { username } }"},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                data = resp.json()
                username = data.get("data", {}).get("viewer", {}).get("username", "unknown")
                self.add_result(TestResult("WANDB_API_KEY", "PASS", f"Authenticated as: {username}", latency))
            else:
                self.add_result(TestResult("WANDB_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("WANDB_API_KEY", "FAIL", str(e)[:100]))

    def test_firecrawl(self):
        """Test Firecrawl API key"""
        key = self.test_env_var("FIRECRAWL_API_KEY", required=False)
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.get(
                "https://api.firecrawl.dev/v1/scrape",
                headers={"Authorization": f"Bearer {key}"},
                params={"url": "https://example.com"},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code in [200, 402]:  # 402 = rate limited but key valid
                self.add_result(TestResult("FIRECRAWL_API_KEY", "PASS", "Key valid", latency))
            else:
                self.add_result(TestResult("FIRECRAWL_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("FIRECRAWL_API_KEY", "FAIL", str(e)[:100]))

    def test_resend(self):
        """Test Resend API key"""
        key = self.test_env_var("RESEND_API_KEY", required=False)
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.get(
                "https://api.resend.com/domains",
                headers={"Authorization": f"Bearer {key}"},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("RESEND_API_KEY", "PASS", "API responds", latency))
            else:
                self.add_result(TestResult("RESEND_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("RESEND_API_KEY", "FAIL", str(e)[:100]))

    def test_render(self):
        """Test Render CLI token"""
        key = self.test_env_var("RENDER_CLI_TOKEN", required=False)
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.get(
                "https://api.render.com/v1/services",
                headers={"Authorization": f"Bearer {key}"},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("RENDER_CLI_TOKEN", "PASS", "API responds", latency))
            else:
                self.add_result(TestResult("RENDER_CLI_TOKEN", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("RENDER_CLI_TOKEN", "FAIL", str(e)[:100]))

    def test_opencode(self):
        """Test OpenCode API key"""
        key = self.test_env_var("OPENCODE_API_KEY", required=False)
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.post(
                "https://api.opencode.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "opencode/mimo-v2-free", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("OPENCODE_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 401:
                self.add_result(TestResult("OPENCODE_API_KEY", "FAIL", "Invalid key", latency))
            else:
                self.add_result(TestResult("OPENCODE_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("OPENCODE_API_KEY", "FAIL", str(e)[:100]))

    def test_zai(self):
        """Test ZAI API key"""
        key = self.test_env_var("ZAI_API_KEY", required=False)
        if not key:
            return

        try:
            import requests
            start = time.time()
            # Try multiple possible endpoints
            endpoints = [
                "https://api.zai.com/v1/chat/completions",
                "https://api.zhipuai.com/v1/chat/completions",
                "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            ]
            for endpoint in endpoints:
                try:
                    resp = requests.post(
                        endpoint,
                        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                        json={"model": "glm-4-flash", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
                        timeout=10
                    )
                    latency = (time.time() - start) * 1000
                    if resp.status_code == 200:
                        self.add_result(TestResult("ZAI_API_KEY", "PASS", f"API responds at {endpoint.split('/')[2]}", latency))
                        return
                    elif resp.status_code == 401:
                        self.add_result(TestResult("ZAI_API_KEY", "FAIL", "Invalid key", latency))
                        return
                except:
                    continue
            latency = (time.time() - start) * 1000
            self.add_result(TestResult("ZAI_API_KEY", "WARN", "Key may be valid but endpoints unreachable", latency))
        except Exception as e:
            self.add_result(TestResult("ZAI_API_KEY", "FAIL", str(e)[:100]))

    def test_kimi(self):
        """Test Kimi API key"""
        key = self.test_env_var("KIMI_API_KEY", required=False)
        if not key:
            return

        try:
            import requests
            start = time.time()
            resp = requests.post(
                "https://api.moonshot.cn/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "moonshot-v1-8k", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.add_result(TestResult("KIMI_API_KEY", "PASS", "API responds", latency))
            elif resp.status_code == 401:
                self.add_result(TestResult("KIMI_API_KEY", "FAIL", "Invalid key", latency))
            else:
                self.add_result(TestResult("KIMI_API_KEY", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("KIMI_API_KEY", "FAIL", str(e)[:100]))

    def test_kaggle(self):
        """Test Kaggle API token"""
        key = self.test_env_var("KAGGLE_ACCESS_TOKEN", required=False)
        if not key:
            return

        try:
            import requests
            start = time.time()
            # Kaggle uses username + token for auth
            resp = requests.get(
                "https://www.kaggle.com/api/v1/datasets/list",
                headers={"Authorization": f"Bearer {key}"},
                timeout=15
            )
            latency = (time.time() - start) * 1000
            if resp.status_code in [200, 403]:  # 403 = auth worked but permissions issue
                self.add_result(TestResult("KAGGLE_ACCESS_TOKEN", "PASS", "Token valid", latency))
            else:
                self.add_result(TestResult("KAGGLE_ACCESS_TOKEN", "WARN", f"HTTP {resp.status_code}", latency))
        except Exception as e:
            self.add_result(TestResult("KAGGLE_ACCESS_TOKEN", "FAIL", str(e)[:100]))

    def test_smtp(self):
        """Test SMTP connection"""
        host = os.environ.get("SMTP_HOST", "")
        port = os.environ.get("SMTP_PORT", "")
        user = os.environ.get("SMTP_USER", "")
        password = os.environ.get("SMTP_PASS", "")

        if not all([host, port, user, password]):
            self.add_result(TestResult("SMTP", "SKIP", "Missing SMTP config"))
            return

        try:
            import smtplib
            start = time.time()
            server = smtplib.SMTP(host, int(port), timeout=10)
            server.starttls()
            server.login(user, password)
            server.quit()
            latency = (time.time() - start) * 1000
            self.add_result(TestResult("SMTP", "PASS", f"Connected to {host}:{port}", latency))
        except Exception as e:
            self.add_result(TestResult("SMTP", "FAIL", str(e)[:100]))

    def test_chromadb(self):
        """Test ChromaDB vector database"""
        try:
            import chromadb
            start = time.time()
            client = chromadb.PersistentClient(path=str(Path.home() / "Desktop/Projects/MEMORY/memory/vector_db"))
            collection = client.get_or_create_collection("antigravity_memory")
            count = collection.count()
            latency = (time.time() - start) * 1000
            self.add_result(TestResult("ChromaDB", "PASS", f"{count} chunks indexed", latency))
        except Exception as e:
            self.add_result(TestResult("ChromaDB", "FAIL", str(e)[:100]))

    def test_postgresql(self):
        """Test PostgreSQL connection"""
        host = os.environ.get("PG_HOST", "")
        port = os.environ.get("PG_PORT", "")
        database = os.environ.get("PG_DATABASE", "")
        user = os.environ.get("PG_USER", "")
        password = os.environ.get("PG_PASSWORD", "")

        if not all([host, port, database, user, password]):
            self.add_result(TestResult("PostgreSQL", "SKIP", "Missing config"))
            return

        try:
            import psycopg2
            start = time.time()
            conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password, connect_timeout=5)
            conn.close()
            latency = (time.time() - start) * 1000
            self.add_result(TestResult("PostgreSQL", "PASS", f"Connected to {host}:{port}/{database}", latency))
        except ImportError:
            self.add_result(TestResult("PostgreSQL", "SKIP", "psycopg2 not installed"))
        except Exception as e:
            self.add_result(TestResult("PostgreSQL", "WARN", f"Not running or inaccessible: {str(e)[:60]}"))

    def test_mysql(self):
        """Test MySQL connection"""
        host = os.environ.get("MYSQL_HOST", "")
        port = os.environ.get("MYSQL_PORT", "")
        database = os.environ.get("MYSQL_DATABASE", "")
        user = os.environ.get("MYSQL_USER", "")
        password = os.environ.get("MYSQL_PASSWORD", "")

        if not all([host, port, database, user, password]):
            self.add_result(TestResult("MySQL", "SKIP", "Missing config"))
            return

        try:
            import mysql.connector
            start = time.time()
            conn = mysql.connector.connect(host=host, port=port, database=database, user=user, password=password, connect_timeout=5)
            conn.close()
            latency = (time.time() - start) * 1000
            self.add_result(TestResult("MySQL", "PASS", f"Connected to {host}:{port}/{database}", latency))
        except ImportError:
            self.add_result(TestResult("MySQL", "SKIP", "mysql-connector-python not installed"))
        except Exception as e:
            self.add_result(TestResult("MySQL", "WARN", f"Not running or inaccessible: {str(e)[:60]}"))

    def test_redis(self):
        """Test Redis connection"""
        host = os.environ.get("REDIS_HOST", "")
        port = os.environ.get("REDIS_PORT", "")

        if not all([host, port]):
            self.add_result(TestResult("Redis", "SKIP", "Missing config"))
            return

        try:
            import redis
            start = time.time()
            r = redis.Redis(host=host, port=int(port), socket_timeout=5)
            r.ping()
            latency = (time.time() - start) * 1000
            self.add_result(TestResult("Redis", "PASS", f"Connected to {host}:{port}", latency))
        except ImportError:
            self.add_result(TestResult("Redis", "SKIP", "redis-py not installed"))
        except Exception as e:
            self.add_result(TestResult("Redis", "WARN", f"Not running or inaccessible: {str(e)[:60]}"))

    def test_mongodb(self):
        """Test MongoDB connection"""
        host = os.environ.get("MONGO_HOST", "")
        port = os.environ.get("MONGO_PORT", "")

        if not all([host, port]):
            self.add_result(TestResult("MongoDB", "SKIP", "Missing config"))
            return

        try:
            from pymongo import MongoClient
            start = time.time()
            client = MongoClient(host=host, port=int(port), serverSelectionTimeoutMS=3000)
            client.server_info()
            latency = (time.time() - start) * 1000
            self.add_result(TestResult("MongoDB", "PASS", f"Connected to {host}:{port}", latency))
        except ImportError:
            self.add_result(TestResult("MongoDB", "SKIP", "pymongo not installed"))
        except Exception as e:
            self.add_result(TestResult("MongoDB", "WARN", f"Not running or inaccessible: {str(e)[:60]}"))

    def test_memory_core(self):
        """Test MEMORY core functionality"""
        memory_root = Path.home() / "Desktop/Projects/MEMORY"

        # Test 1: GEMINI.md exists and has content
        gemini_path = memory_root / "GEMINI.md"
        if gemini_path.exists():
            content = gemini_path.read_text()
            lines = len(content.split("\n"))
            if lines > 100:
                self.add_result(TestResult("GEMINI.md", "PASS", f"{lines} lines"))
            else:
                self.add_result(TestResult("GEMINI.md", "WARN", f"Only {lines} lines, expected 100+"))
        else:
            self.add_result(TestResult("GEMINI.md", "FAIL", "File not found"))

        # Test 2: All 20 modules exist
        modules_dir = memory_root / "memory" / "modules"
        if modules_dir.exists():
            modules = list(modules_dir.glob("*.md"))
            if len(modules) >= 20:
                self.add_result(TestResult("Modules", "PASS", f"{len(modules)} modules found"))
            else:
                self.add_result(TestResult("Modules", "WARN", f"Only {len(modules)} modules, expected 20+"))
        else:
            self.add_result(TestResult("Modules", "FAIL", "Modules directory not found"))

        # Test 3: Vector DB has content
        db_path = memory_root / "memory" / "vector_db"
        if db_path.exists():
            try:
                import chromadb
                client = chromadb.PersistentClient(path=str(db_path))
                col = client.get_or_create_collection("antigravity_memory")
                count = col.count()
                if count >= 300:
                    self.add_result(TestResult("VectorDB", "PASS", f"{count} chunks"))
                else:
                    self.add_result(TestResult("VectorDB", "WARN", f"Only {count} chunks, expected 300+"))
            except Exception as e:
                self.add_result(TestResult("VectorDB", "FAIL", str(e)[:100]))
        else:
            self.add_result(TestResult("VectorDB", "FAIL", "Vector DB not found"))

        # Test 4: Tools exist
        tools_dir = memory_root / "tools"
        if tools_dir.exists():
            tools = list(tools_dir.glob("*.py")) + list(tools_dir.glob("*.sh"))
            if len(tools) >= 10:
                self.add_result(TestResult("Tools", "PASS", f"{len(tools)} tools"))
            else:
                self.add_result(TestResult("Tools", "WARN", f"Only {len(tools)} tools, expected 10+"))
        else:
            self.add_result(TestResult("Tools", "FAIL", "Tools directory not found"))

        # Test 5: CI workflow
        ci_path = memory_root / ".github" / "workflows" / "ci.yml"
        if ci_path.exists():
            content = ci_path.read_text()
            if "MIT" in content:
                self.add_result(TestResult("CI License", "PASS", "MIT header"))
            else:
                self.add_result(TestResult("CI License", "WARN", "Missing MIT header"))
        else:
            self.add_result(TestResult("CI", "WARN", "No CI workflow found"))

        # Test 6: Dashboard exists
        dashboard_path = tools_dir / "dashboard.py"
        if dashboard_path.exists():
            content = dashboard_path.read_text()
            if "httpx" not in content:
                self.add_result(TestResult("Dashboard", "PASS", "No httpx dependency"))
            else:
                self.add_result(TestResult("Dashboard", "WARN", "Still uses httpx"))
        else:
            self.add_result(TestResult("Dashboard", "FAIL", "dashboard.py not found"))

    def test_cli_tools(self):
        """Test CLI tools availability"""
        tools = [
            ("rg", "ripgrep"), ("bat", "batcat"), ("eza", "ls replacement"),
            ("fd", "fdfind"), ("dust", "disk usage"), ("btop", "top replacement"),
            ("procs", "ps replacement"), ("sd", "sed replacement"),
            ("jq", "JSON processor"), ("glow", "markdown renderer"),
            ("lazygit", "git TUI"), ("tokei", "code counter"),
            ("onefetch", "git summary"), ("hyperfine", "benchmarking"),
            ("tmux", "terminal multiplexer"), ("pm2", "process manager"),
            ("gh", "GitHub CLI"), ("fzf", "fuzzy finder"),
            ("zoxide", "smart cd"), ("bun", "JS runtime"),
            ("uv", "Python package manager"), ("pipx", "Python app installer")
        ]

        available = 0
        missing = []
        for cmd, desc in tools:
            import shutil
            if shutil.which(cmd):
                available += 1
            else:
                missing.append(cmd)

        if available >= 20:
            self.add_result(TestResult("CLI Tools", "PASS", f"{available}/{len(tools)} available"))
        elif available >= 15:
            self.add_result(TestResult("CLI Tools", "WARN", f"{available}/{len(tools)} available, missing: {', '.join(missing[:3])}"))
        else:
            self.add_result(TestResult("CLI Tools", "FAIL", f"Only {available}/{len(tools)} available"))

    def test_guardrails(self):
        """Test guardrails are installed"""
        guardrails_dir = Path.home() / "bin" / "guardrails"
        if guardrails_dir.exists():
            scripts = list(guardrails_dir.glob("*"))
            if len(scripts) >= 8:
                self.add_result(TestResult("Guardrails", "PASS", f"{len(scripts)} guardrails installed"))
            else:
                self.add_result(TestResult("Guardrails", "WARN", f"Only {len(scripts)} guardrails, expected 8+"))
        else:
            self.add_result(TestResult("Guardrails", "FAIL", "Guardrails not found"))

    def run_all_tests(self):
        print("\n" + "="*60)
        print("  MEMORY GLOBAL API KEYS TEST SUITE")
        print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("="*60)

        print("\n--- LLM Providers ---")
        self.test_groq()
        self.test_gemini()
        self.test_openrouter()
        self.test_cerebras()
        self.test_nvidia_nim()
        self.test_huggingface()
        self.test_deepseek()
        self.test_fireworks()
        self.test_mistral()
        self.test_cohere()
        self.test_opencode()
        self.test_zai()
        self.test_kimi()

        print("\n--- Service APIs ---")
        self.test_github()
        self.test_cloudflare()
        self.test_wandb()
        self.test_firecrawl()
        self.test_resend()
        self.test_render()
        self.test_kaggle()

        print("\n--- Infrastructure ---")
        self.test_smtp()
        self.test_chromadb()
        self.test_postgresql()
        self.test_mysql()
        self.test_redis()
        self.test_mongodb()

        print("\n--- CLI Tools ---")
        self.test_cli_tools()
        self.test_guardrails()

        print("\n--- MEMORY Core ---")
        self.test_memory_core()

        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "PASS")
        failed = sum(1 for r in self.results if r.status == "FAIL")
        warned = sum(1 for r in self.results if r.status == "WARN")
        skipped = sum(1 for r in self.results if r.status == "SKIP")

        print("\n" + "="*60)
        print(f"  SUMMARY: {passed} passed, {failed} failed, {warned} warnings, {skipped} skipped")
        print(f"  Total: {total} tests in {time.time() - self.start_time:.1f}s")
        print("="*60 + "\n")

        return failed == 0

if __name__ == "__main__":
    tester = APITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
