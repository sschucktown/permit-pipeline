from typing import NamedTuple, Dict
import hashlib

class FetchResult(NamedTuple):
    url: str
    content_type: str
    body: bytes
    headers: Dict[str, str]

class Fetcher:
    def fetch(self, url: str) -> FetchResult:
        raise NotImplementedError

class MockFetcher(Fetcher):
    def fetch(self, url: str) -> FetchResult:
        html = f"""<html><body>
        <h1>City of Charleston — HVAC Permit</h1>
        <p>Permit required for: new HVAC, replacements over 3 tons, heat pumps.</p>
        <p>Fee: $85 base + $5 per ton.</p>
        <p>Submit online at: https://example.charleston.gov/permit/HVAC</p>
        <p>Contact: permits@charleston-sc.gov, (843) 555-1234</p>
        <p>Effective: 2024-02-01</p>
        </body></html>"""
        return FetchResult(
            url=url, content_type="text/html", body=html.encode("utf-8"),
            headers={"ETag": hashlib.md5(html.encode()).hexdigest()}
        )
