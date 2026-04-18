from __future__ import annotations

from dataclasses import dataclass
import html
import re
from urllib.parse import urljoin

import requests


@dataclass
class ScrapedBook:
    title: str
    book_url: str
    price: float | None
    rating: float | None
    description: str
    category: str
    image_url: str
def _parse_price(price_text: str) -> float | None:
    try:
        return float(price_text.replace("£", "").strip())
    except Exception:
        return None


def _parse_rating(pod_class: str) -> float | None:
    mapping = {
        "One": 1.0,
        "Two": 2.0,
        "Three": 3.0,
        "Four": 4.0,
        "Five": 5.0,
    }
    for key, value in mapping.items():
        if key in pod_class:
            return value
    return None


def _fetch_html(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def _extract_listing_summaries(page_html: str, page_url: str) -> tuple[list[dict], str | None]:
    summaries: list[dict] = []

    pod_blocks = re.findall(r"<article\s+class=\"product_pod\".*?</article>", page_html, flags=re.DOTALL)
    for block in pod_blocks:
        anchor_match = re.search(
            r"<h3>\s*<a\s+[^>]*href=\"([^\"]+)\"[^>]*title=\"([^\"]+)\"",
            block,
            flags=re.DOTALL,
        )
        if not anchor_match:
            continue

        href, title = anchor_match.groups()
        detail_url = urljoin(page_url, html.unescape(href))
        title = html.unescape(title).strip()

        price_match = re.search(r"<p\s+class=\"price_color\">\s*([^<]+)\s*</p>", block)
        price_text = html.unescape(price_match.group(1)).strip() if price_match else ""

        rating_match = re.search(r"<p\s+class=\"star-rating\s+([^\"]+)\"", block)
        rating_class = rating_match.group(1).strip() if rating_match else ""

        summaries.append(
            {
                "title": title,
                "book_url": detail_url,
                "price": _parse_price(price_text),
                "rating": _parse_rating(rating_class),
            }
        )

    next_match = re.search(r"<li\s+class=\"next\">\s*<a\s+href=\"([^\"]+)\"", page_html)
    next_url = urljoin(page_url, html.unescape(next_match.group(1))) if next_match else None
    return summaries, next_url


def _extract_description(detail_html: str) -> str:
    match = re.search(
        r"id=\"product_description\".*?</h2>\s*<p>(.*?)</p>",
        detail_html,
        flags=re.DOTALL,
    )
    if not match:
        return ""

    text = re.sub(r"<[^>]+>", "", match.group(1))
    return html.unescape(text).strip()


def _extract_category(detail_html: str) -> str:
    categories = re.findall(r"<ul\s+class=\"breadcrumb\".*?</ul>", detail_html, flags=re.DOTALL)
    if not categories:
        return ""

    anchor_texts = re.findall(r"<a[^>]*>(.*?)</a>", categories[0], flags=re.DOTALL)
    if len(anchor_texts) < 3:
        return ""
    return html.unescape(re.sub(r"<[^>]+>", "", anchor_texts[2])).strip()


def _extract_image_url(detail_html: str, detail_url: str) -> str:
    match = re.search(r"<div\s+class=\"item active\".*?<img\s+[^>]*src=\"([^\"]+)\"", detail_html, flags=re.DOTALL)
    if not match:
        return ""
    return urljoin(detail_url, html.unescape(match.group(1)))


def scrape_books(base_url: str, max_pages: int = 3) -> list[ScrapedBook]:
    summaries: list[dict] = []
    next_url: str | None = base_url

    pages_done = 0
    while next_url and pages_done < max_pages:
        page_html = _fetch_html(next_url)
        page_summaries, next_url = _extract_listing_summaries(page_html, next_url)
        summaries.extend(page_summaries)
        pages_done += 1

    results: list[ScrapedBook] = []
    for summary in summaries:
        detail_url = summary["book_url"]
        detail_html = _fetch_html(detail_url)

        results.append(
            ScrapedBook(
                title=summary["title"],
                book_url=detail_url,
                price=summary["price"],
                rating=summary["rating"],
                description=_extract_description(detail_html),
                category=_extract_category(detail_html),
                image_url=_extract_image_url(detail_html, detail_url),
            )
        )

    return results
