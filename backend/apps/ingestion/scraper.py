from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class ScrapedBook:
    title: str
    book_url: str
    price: float | None
    rating: float | None
    description: str
    category: str
    image_url: str


def _build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


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


def scrape_books(base_url: str, max_pages: int = 3) -> list[ScrapedBook]:
    driver = _build_driver()
    summaries: list[dict] = []

    try:
        driver.get(base_url)
        pages_done = 0

        while pages_done < max_pages:
            pods = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
            for pod in pods:
                anchor = pod.find_element(By.CSS_SELECTOR, "h3 a")
                title = anchor.get_attribute("title")
                detail_url = urljoin(driver.current_url, anchor.get_attribute("href"))
                price_text = pod.find_element(By.CSS_SELECTOR, "p.price_color").text
                rating_class = pod.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class")
                summaries.append(
                    {
                        "title": title,
                        "book_url": detail_url,
                        "price": _parse_price(price_text),
                        "rating": _parse_rating(rating_class),
                    }
                )

            next_buttons = driver.find_elements(By.CSS_SELECTOR, "li.next a")
            if not next_buttons:
                break
            next_url = urljoin(driver.current_url, next_buttons[0].get_attribute("href"))
            driver.get(next_url)
            pages_done += 1

        results: list[ScrapedBook] = []
        for summary in summaries:
            driver.get(summary["book_url"])

            description = ""
            try:
                desc_anchor = driver.find_element(By.ID, "product_description")
                description = desc_anchor.find_element(By.XPATH, "following-sibling::p").text
            except Exception:
                description = ""

            category = ""
            try:
                breadcrumb = driver.find_elements(By.CSS_SELECTOR, "ul.breadcrumb li a")
                if len(breadcrumb) >= 3:
                    category = breadcrumb[2].text.strip()
            except Exception:
                category = ""

            image_url = ""
            try:
                image = driver.find_element(By.CSS_SELECTOR, "div.item.active img")
                image_url = urljoin(driver.current_url, image.get_attribute("src"))
            except Exception:
                image_url = ""

            results.append(
                ScrapedBook(
                    title=summary["title"],
                    book_url=summary["book_url"],
                    price=summary["price"],
                    rating=summary["rating"],
                    description=description,
                    category=category,
                    image_url=image_url,
                )
            )

        return results
    finally:
        driver.quit()
