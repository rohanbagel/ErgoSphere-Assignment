from __future__ import annotations

import os
import hashlib
from functools import lru_cache


def get_embedding_backend() -> str:
    configured = os.getenv("EMBEDDING_BACKEND", "").strip().lower()
    if configured in {"hash", "sentence-transformers"}:
        return configured

    # Render free instances are memory-constrained, so default to hash embeddings there.
    if os.getenv("RENDER"):
        return "hash"
    return "sentence-transformers"

@lru_cache(maxsize=1)
def get_embedding_model():
    if get_embedding_backend() != "sentence-transformers":
        raise RuntimeError("Sentence-transformers backend is disabled")

    from sentence_transformers import SentenceTransformer

    model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    return SentenceTransformer(model_name)


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    if get_embedding_backend() == "hash":
        dimensions = int(os.getenv("EMBEDDING_HASH_DIM", "128"))
        return [_hash_embed(text, dimensions=dimensions) for text in texts]

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
