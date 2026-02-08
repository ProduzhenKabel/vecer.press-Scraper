import aiohttp
from bs4 import BeautifulSoup
from scraper.models import Record
import hashlib

BASE = "https://www.vecer.press"

class Parser:
    async def parse(self, urls: list[str]) -> list[Record]:

        records = []

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            for url in urls:

                try:
                    async with session.get(url) as res:
                        html = await res.text()
                except Exception:
                    continue

                soup = BeautifulSoup(html, "html.parser")


                title_tag = soup.select_one("h1.entry-title, h1.post-title, h1")
                title = title_tag.get_text(strip=True) if title_tag else ""

                paragraphs = []

                selectors = [
                    "div.entry-content p",
                    "div.post-content p",
                    "article p",
                    "div.td-post-content p",
                    ".wp-block-post-content p"
                ]

                for sel in selectors:
                    content_tags = soup.select(sel)
                    if content_tags:
                        paragraphs = [
                            p.get_text(strip=True)
                            for p in content_tags
                            if p.get_text(strip=True)
                        ]
                        if paragraphs:
                            break

                content = "\n".join(paragraphs)


                time_tag = soup.select_one("time[datetime]")
                if time_tag:
                    published_at = time_tag.get("datetime")
                else:
                    time_tag = soup.select_one("time, span.post-date")
                    published_at = time_tag.get_text(strip=True) if time_tag else None


                cat_tag = soup.select_one("a[rel='category tag'], .td-post-category a")
                category = cat_tag.get_text(strip=True) if cat_tag else ""

                rid = hashlib.md5(url.encode()).hexdigest()

                records.append(Record(
                    id=rid,
                    title=title,
                    site_url=BASE,
                    page_url=url,
                    content=content,
                    published_at=published_at,
                    categories=[category] if category else []
                ))

        return records
