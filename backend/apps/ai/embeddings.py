from __future__ import annotations

import os
import hashlib
from functools import lru_cache

@lru_cache(maxsize=1)
def get_embedding_model():
    from sentence_transformers import SentenceTransformer

    model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    return SentenceTransformer(model_name)


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    try:
        model = get_embedding_model()
        vectors = model.encode(texts, normalize_embeddings=True)
        return vectors.tolist()
    except Exception:
        return [_hash_embed(text) for text in texts]


def embed_text(text: str) -> list[float]:
    vectors = embed_texts([text])
    return vectors[0] if vectors else []


def _hash_embed(text: str, dimensions: int = 128) -> list[float]:
    normalized = (text or "").strip().lower()
    if not normalized:
        return [0.0] * dimensions

    values = [0.0] * dimensions
    tokens = normalized.split()
    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        for idx in range(dimensions):
            values[idx] += digest[idx % len(digest)] / 255.0

    length = max(len(tokens), 1)
    return [value / length for value in values]
