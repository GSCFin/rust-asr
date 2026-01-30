"""LLM client for Google Generative AI (Gemini) integration."""

import os
import json
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class GeminiClient:
    """Client for Google Generative AI (Gemini) API."""
    
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        api_url: str | None = None,
    ):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = model or os.getenv("GOOGLE_MODEL", "gemini-3-pro-preview")
        self.api_url = api_url or os.getenv(
            "GOOGLE_API_URL",
            "https://generativelanguage.googleapis.com"
        )
        
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY not set. "
                "Set it in .env or pass api_key parameter."
            )
    
    @property
    def endpoint(self) -> str:
        """Get the API endpoint for text generation."""
        return f"{self.api_url}/v1beta/models/{self.model}:generateContent"
    
    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """Generate text using Gemini API.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system instruction
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        contents = []
        
        if system_prompt:
            contents.append({
                "role": "user",
                "parts": [{"text": f"System: {system_prompt}"}]
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Understood. I'll follow those instructions."}]
            })
        
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                json=payload,
                params={"key": self.api_key},
                headers={"Content-Type": "application/json"},
                timeout=300.0,
            )
            response.raise_for_status()
            data = response.json()
        
        # Extract text from response
        try:
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
        except (KeyError, IndexError):
            pass
        
        return ""
    
    def generate_sync(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """Synchronous version of generate."""
        import asyncio
        return asyncio.run(
            self.generate(prompt, system_prompt, temperature, max_tokens)
        )


def get_client() -> GeminiClient:
    """Get a configured Gemini client instance."""
    return GeminiClient()


async def analyze_architecture(
    codebase_context: str,
    analysis_type: str = "summary",
) -> str:
    """Use LLM to analyze architecture.
    
    Args:
        codebase_context: The mapped codebase text
        analysis_type: One of 'summary', 'c4', 'patterns', 'ddd'
        
    Returns:
        Analysis result as markdown
    """
    from rust_asr.ai import prompts
    
    client = get_client()
    
    if analysis_type == "c4":
        prompt = prompts.C4_CONTEXT_PROMPT.format(
            codebase_context=codebase_context,
            project_name="Project"
        )
    elif analysis_type == "patterns":
        prompt = prompts.PATTERN_ANALYSIS_PROMPT.format(
            codebase_context=codebase_context,
            static_patterns="See codebase context"
        )
    elif analysis_type == "ddd":
        prompt = prompts.DDD_BOUNDED_CONTEXT_PROMPT.format(
            codebase_context=codebase_context,
            module_tree="See codebase context"
        )
    else:  # summary
        prompt = prompts.ARCHITECTURE_SUMMARY_PROMPT.format(
            codebase_context=codebase_context,
            dependency_graph="See codebase",
            patterns="See codebase",
            metrics="See codebase"
        )
    
    system_prompt = (
        "You are a senior Rust software architect. "
        "Analyze codebases and provide clear, actionable insights. "
        "Use Mermaid diagrams when appropriate."
    )
    
    return await client.generate(prompt, system_prompt)
