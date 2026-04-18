from __future__ import annotations

import json
import os

from openai import OpenAI


def get_groq_client() -> OpenAI:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured")
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


def get_groq_model() -> str:
    return os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


def _chat(messages: list[dict], temperature: float = 0.2, max_tokens: int = 700) -> str:
    client = get_groq_client()
    response = client.chat.completions.create(
        model=get_groq_model(),
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return (response.choices[0].message.content or "").strip()


def generate_insights(title: str, author: str, description: str) -> dict:
    prompt = (
        "Return ONLY valid JSON with keys summary, genre, recommendation. "
        "Keep summary concise (2-3 sentences), genre as short label, "
        "and recommendation as one actionable line."
    )
    user_text = (
        f"Title: {title}\n"
        f"Author: {author}\n"
        f"Description: {description}\n"
    )
    fallback = {
        "summary": (description or "")[:280],
        "genre": "General",
        "recommendation": "If you enjoy this style, explore similar books in the same category.",
    }

    try:
        raw = _chat(
            [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=0.1,
            max_tokens=350,
        )
    except Exception:
        return fallback

    try:
        parsed = json.loads(raw)
        return {
            "summary": str(parsed.get("summary", fallback["summary"])).strip(),
            "genre": str(parsed.get("genre", fallback["genre"])).strip(),
            "recommendation": str(parsed.get("recommendation", fallback["recommendation"])).strip(),
        }
    except Exception:
        return fallback


def answer_from_context(question: str, context_blocks: list[dict]) -> str:
    context_text = "\n\n".join(
        f"[{item['source_id']}] {item['text']}" for item in context_blocks
    )
    messages = [
        {
            "role": "system",
            "content": (
                "You are a grounded assistant. Answer only from the provided context. "
                "If context is insufficient, clearly say so. "
                "Cite sources inline using [S1], [S2] style."
            ),
        },
        {
            "role": "user",
            "content": f"Question: {question}\n\nContext:\n{context_text}",
        },
    ]
    try:
        return _chat(messages, temperature=0.1, max_tokens=800)
    except Exception:
        snippets = [item["text"] for item in context_blocks[:3]]
        if snippets:
            return "Groq is not configured, so here is a context-based fallback answer: " + " ".join(snippets)
        return "Groq is not configured and no relevant context was retrieved."
