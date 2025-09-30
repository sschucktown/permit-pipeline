from typing import Protocol
from ..fetcher import FetchResult

class Adapter(Protocol):
    vendor: str
    def accepts(self, result: FetchResult) -> bool: ...
    def extract_raw(self, result: FetchResult) -> dict: ...
