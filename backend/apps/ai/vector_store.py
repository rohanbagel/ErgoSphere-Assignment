from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

@lru_cache(maxsize=1)
def get_collection():
    import chromadb

    mode = os.getenv("CHROMA_MODE", "local").strip().lower()
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
    collection_name = os.getenv("CHROMA_COLLECTION", "book_chunks")

    if mode == "cloud":
        api_key = os.getenv("CHROMA_API_KEY", "").strip()
        tenant = os.getenv("CHROMA_TENANT", "").strip()
        database = os.getenv("CHROMA_DATABASE", "").strip()
        if api_key and tenant and database:
            client = chromadb.CloudClient(
                api_key=api_key,
                tenant=tenant,
                database=database,
            )
        else:
            raise ValueError(
                "CHROMA_MODE is cloud but CHROMA_API_KEY, CHROMA_TENANT, or CHROMA_DATABASE is missing"
            )
    else:
        base_path = Path(__file__).resolve().parents[2]
        persist_path = (base_path / persist_dir).resolve()
        persist_path.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(persist_path))

    return client.get_or_create_collection(name=collection_name)


def upsert_chunks(ids: list[str], documents: list[str], embeddings: list[list[float]], metadatas: list[dict]):
    if not ids:
        return
    collection = get_collection()
    collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)


def query_chunks(query_embedding: list[float], n_results: int = 5, where: dict | None = None):
    collection = get_collection()
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where,
        include=["documents", "metadatas", "distances"],
    )
