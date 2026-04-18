from __future__ import annotations

from django.conf import settings

from apps.ai.rag import build_index_for_book, generate_and_save_insights
from apps.books.models import Book

from .scraper import scrape_books


DEFAULT_SOURCE = "books_to_scrape"


def ingest_books(start_url: str, max_pages: int = 3, max_books: int = 5) -> dict:
    records = scrape_books(base_url=start_url, max_pages=max_pages)[:max_books]

    processed = 0
    indexed = 0
    for item in records:
        book, _created = Book.objects.update_or_create(
            book_url=item.book_url,
            defaults={
                "title": item.title,
                "author": "Unknown",
                "category": item.category,
                "rating": item.rating,
                "review_count": 0,
                "price": item.price,
                "description": item.description,
                "image_url": item.image_url,
                "source": DEFAULT_SOURCE,
            },
        )
        try:
            generate_and_save_insights(book)
        except Exception:
            # Demo path should still ingest and index even if AI is unavailable.
            pass
        indexed += build_index_for_book(book)
        processed += 1

    return {
        "processed_books": processed,
        "indexed_chunks": indexed,
        "source": start_url,
    }


def get_default_scraper_url() -> str:
    return getattr(settings, "SCRAPER_BASE_URL", "https://books.toscrape.com/")
