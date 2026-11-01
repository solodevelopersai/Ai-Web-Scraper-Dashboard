from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from database import DatabaseManager
from pipeline import DataPipeline
from scraper import WebScraper


def main() -> None:
    load_dotenv()

    target_url = os.getenv("TARGET_URL", "https://example.com")
    selectors = {
        "title": os.getenv("SELECTOR_TITLE", "title"),
        "content": os.getenv("SELECTOR_CONTENT", "body"),
    }

    print("AI-Powered Web Scraping & Data Pipeline Dashboard")
    print(f"Target URL: {target_url}\n")

    scraper = WebScraper(target_url=target_url)
    raw_data = scraper.fetch_and_extract(selectors=selectors)

    if not raw_data:
        print("No data was extracted from the target page.")
        return

    pipeline = DataPipeline()
    cleaned_data = pipeline.process(raw_data)

    db = DatabaseManager()
    db.initialize_database()
    inserted_records = db.insert_scraped_data(cleaned_data)

    print(f"Inserted {inserted_records} record(s) into the local SQLite database.")
    print("\nScraped Data Preview:")
    for item in cleaned_data[:5]:
        print(item)


if __name__ == "__main__":
    main()
