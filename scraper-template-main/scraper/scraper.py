from scraper.fetcher import Fetcher
from scraper.parser import Parser
from store.factory import StoreFactory
from config.scraper_settings import settings

class Scraper:
    def __init__(self):
        self.fetcher = Fetcher()
        self.parser = Parser()
        self.store = StoreFactory.create()

    async def run(self):
        metadata = await self.fetcher.fetch_metadata()
        raw = await self.fetcher.fetch_all(metadata)
        records = await self.parser.parse(raw)
        self.store.save_records(records)
