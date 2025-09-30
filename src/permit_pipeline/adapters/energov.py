from .base import Adapter
from ..fetcher import FetchResult
from bs4 import BeautifulSoup

class EnerGovAdapter:
    vendor = "energov"
    def accepts(self, result: FetchResult) -> bool:
        return True

    def extract_raw(self, result: FetchResult) -> dict:
        soup = BeautifulSoup(result.body, "html.parser")
        text = soup.get_text(" ", strip=True)
        return {
            "source_url": result.url,
            "content_type": result.content_type,
            "text": text,
            "headers": dict(result.headers),
        }
