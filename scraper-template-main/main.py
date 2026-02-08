import asyncio
import json
from scraper.fetcher import Fetcher
from scraper.parser import Parser

async def main():
    fetcher = Fetcher()
    parser = Parser()

    urls = await fetcher.fetch_metadata()
    print("URLs found:", len(urls))
    raw = await fetcher.fetch_all(urls)
    records = await parser.parse(raw)


    with open("rezultati.json", "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in records], f, ensure_ascii=False, indent=4)

asyncio.run(main())
