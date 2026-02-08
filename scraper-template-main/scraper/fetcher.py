from typing import List
import feedparser
from scraper.models import Record
import hashlib

BASE = "https://www.vecer.press"

class Fetcher:
    async def fetch_metadata(self) -> List[str]:

        feed_url = BASE + "/feed/"
        feed = feedparser.parse(feed_url)

        urls = []
        for entry in feed.entries:
            urls.append(entry.link)

        return urls

    async def fetch_all(self, metadata: List[str]) -> List[str]:

        return metadata
