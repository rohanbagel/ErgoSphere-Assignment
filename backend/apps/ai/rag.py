from __future__ import annotations

from dataclasses import dataclass

from apps.books.models import Book, BookChunk, BookInsight, QAHistory

from .chunking import chunk_text


@dataclass
class Citation:
    book_id: int
    book_title: str
    book_url: str
    chunk_id: str
    excerpt: str


def build_index_for_book(book: Book) -> int:
    from .embeddings import embed_texts
    from .vector_store import upsert_chunks

    raw_text = f"{book.title}\n{book.author}\n{book.category}\n{book.description}"
    chunks = chunk_text(raw_text)
    if not chunks:
        return 0

    BookChunk.objects.filter(book=book).delete()

    ids: list[str] = []
    docs: list[str] = []
    metadatas: list[dict] = []
    model_chunks: list[BookChunk] = []

    for piece in chunks:
        chunk_id = f"book_{book.id}_chunk_{piece.index}"
        ids.append(chunk_id)
        docs.append(piece.text)
        metadatas.append(
            {
                "book_id": book.id,
                "book_title": book.title,
                "book_url": book.book_url,
                "chunk_index": piece.index,
            }
        )
        model_chunks.append(
            BookChunk(
                book=book,
                chunk_id=chunk_id,
                chunk_index=piece.index,
                chunk_text=piece.text,
                token_count=max(1, len(piece.text) // 4),
            )
        )

    vectors = embed_texts(docs)
    upsert_chunks(ids=ids, documents=docs, embeddings=vectors, metadatas=metadatas)
    BookChunk.objects.bulk_create(model_chunks)
    return len(model_chunks)


def generate_and_save_insights(book: Book) -> dict:
    from .llm import generate_insights, get_groq_model

    result = generate_insights(book.title, book.author, book.description)
    BookInsight.objects.update_or_create(
        book=book,
        defaults={
            "summary_text": result["summary"],
            "genre_label": result["genre"],
            "recommendation_text": result["recommendation"],
            "generated_by_model": get_groq_model(),
        },
    )
    book.category = result["genre"] or book.category
    book.insights_ready = True
    book.save(update_fields=["category", "insights_ready", "updated_at"])
    return result


def _to_citations(payload: dict) -> list[Citation]:
    metadatas = payload.get("metadatas", [[]])[0]
    documents = payload.get("documents", [[]])[0]
    ids = payload.get("ids", [[]])[0]

    citations: list[Citation] = []
    for idx, metadata in enumerate(metadatas):
        if not metadata:
            continue
        citations.append(
            Citation(
                book_id=int(metadata.get("book_id", 0)),
                book_title=str(metadata.get("book_title", "")),
                book_url=str(metadata.get("book_url", "")),
                chunk_id=str(ids[idx] if idx < len(ids) else ""),
                excerpt=str(documents[idx] if idx < len(documents) else "")[:280],
            )
        )
    return citations


def ask_question(question: str, book_id: int | None = None, top_k: int = 5) -> dict:
    from .embeddings import embed_text
    from .llm import answer_from_context
    from .vector_store import query_chunks

    query_vector = embed_text(question)
    where = {"book_id": int(book_id)} if book_id else None
    hits = query_chunks(query_embedding=query_vector, n_results=top_k, where=where)

    citations = _to_citations(hits)
    context_blocks = [
        {"source_id": f"S{i + 1}", "text": item.excerpt}
        for i, item in enumerate(citations)
    ]
    answer = answer_from_context(question, context_blocks)

    QAHistory.objects.create(
        question=question,
        book_id=book_id,
        answer=answer,
        citations_count=len(citations),
    )

    return {
        "answer": answer,
        "citations": [
            {
                "book_id": c.book_id,
                "book_title": c.book_title,
                "book_url": c.book_url,
                "chunk_id": c.chunk_id,
                "excerpt": c.excerpt,
            }
            for c in citations
        ],
        "retrieval": {
            "top_k": top_k,
            "hits": len(citations),
        },
    }


def get_recommendations(book: Book, limit: int = 5) -> list[dict]:
    from .embeddings import embed_text
    from .vector_store import query_chunks

    query_vector = embed_text(f"{book.title} {book.description}")
    results = query_chunks(query_embedding=query_vector, n_results=limit * 5)
    citations = _to_citations(results)

    seen: set[int] = {book.id}
    ranked: list[dict] = []

    for item in citations:
        if item.book_id in seen:
            continue
        try:
            target = Book.objects.get(id=item.book_id)
        except Book.DoesNotExist:
            continue
        seen.add(item.book_id)
        ranked.append(
            {
                "id": target.id,
                "title": target.title,
                "author": target.author,
                "score": 0.0,
                "reason": f"Similar themes found in chunk {item.chunk_id}",
            }
        )
        if len(ranked) >= limit:
            break

    return ranked
