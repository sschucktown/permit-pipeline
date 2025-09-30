import requests
import time
import hashlib
from typing import NamedTuple, Dict, Optional


class FetchResult(NamedTuple):
    url: str
    content_type: str
    body: bytes
    headers: Dict[str, str]


class Fetcher:
    def fetch(self, url: str) -> FetchResult:
        raise NotImplementedError


class HttpFetcher(Fetcher):
    """
    Polite HTTP fetcher with retry, timeout, and conditional GET (ETag/Last-Modified).
    """

    def __init__(self, user_agent: str = "PermitGetBot/0.1 (+support@permitget.com)",
                 max_retries: int = 3,
                 backoff: float = 1.5,
                 timeout: int = 10):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})
        self.max_retries = max_retries
        self.backoff = backoff
        self.timeout = timeout

        # Track cache for conditional requests
        self.etags: Dict[str, str] = {}
        self.last_modified: Dict[str, str] = {}

    def fetch(self, url: str) -> FetchResult:
        retries = 0
        while True:
            headers = {}
            if url in self.etags:
                headers["If-None-Match"] = self.etags[url]
            if url in self.last_modified:
                headers["If-Modified-Since"] = self.last_modified[url]

            try:
                resp = self.session.get(url, headers=headers, timeout=self.timeout)

                if resp.status_code == 304:
                    # Not modified → return empty body but preserve headers
                    return FetchResult(
                        url=url,
                        content_type=resp.headers.get("Content-Type", "text/html"),
                        body=b"",
                        headers=dict(resp.headers)
                    )

                resp.raise_for_status()

                # Cache conditional headers
                if "ETag" in resp.headers:
                    self.etags[url] = resp.headers["ETag"]
                if "Last-Modified" in resp.headers:
                    self.last_modified[url] = resp.headers["Last-Modified"]

                return FetchResult(
                    url=url,
                    content_type=resp.headers.get("Content-Type", "text/html"),
                    body=resp.content,
                    headers=dict(resp.headers),
                )

            except Exception as e:
                retries += 1
                if retries > self.max_retries:
                    raise
                time.sleep(self.backoff * retries)
