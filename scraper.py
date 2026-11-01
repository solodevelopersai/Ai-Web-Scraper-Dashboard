from __future__ import annotations

import re
from typing import Any

import requests
from bs4 import BeautifulSoup


class WebScraper:
    """Simple, modular web scraping utility for extracting target page content."""

    def __init__(self, target_url: str, timeout: int = 20) -> None:
        self.target_url = target_url
        self.timeout = timeout

    def fetch_page(self) -> str:
        response = requests.get(self.target_url, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def extract_text(self, html: str, selector: str = "body") -> str:
        soup = BeautifulSoup(html, "html.parser")
        element = soup.select_one(selector)
        if element is None:
            return ""

        text = element.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text)
        return text

    def fetch_and_extract(self, selectors: dict[str, str] | None = None) -> list[dict[str, Any]]:
        html = self.fetch_page()
        soup = BeautifulSoup(html, "html.parser")

        selector_map = selectors or {"title": "title", "content": "body"}
        extracted: list[dict[str, Any]] = []

        for field_name, selector in selector_map.items():
            value = ""
            element = soup.select_one(selector)
            if element is not None:
                value = element.get_text(" ", strip=True)
                value = re.sub(r"\s+", " ", value)
            extracted.append({"field": field_name, "value": value})

        return extracted
