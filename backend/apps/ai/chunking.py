from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    index: int


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> list[Chunk]:
    cleaned = " ".join((text or "").split())
    if not cleaned:
        return []

    if overlap >= chunk_size:
        overlap = max(0, chunk_size // 4)

    chunks: list[Chunk] = []
    start = 0
    idx = 0
    text_len = len(cleaned)

    while start < text_len:
        end = min(text_len, start + chunk_size)
        piece = cleaned[start:end].strip()
        if piece:
            chunks.append(Chunk(text=piece, index=idx))
            idx += 1
        if end >= text_len:
            break
        start = max(end - overlap, start + 1)

    return chunks
