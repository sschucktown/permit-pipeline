from ..fetcher import FetchResult

class TylerAdapter:
    vendor = "tyler"
    def accepts(self, result: FetchResult) -> bool:
        return True
    def extract_raw(self, result: FetchResult) -> dict:
        return {
            "source_url": result.url,
            "content_type": result.content_type,
            "text": result.body.decode("utf-8", "ignore"),
            "headers": dict(result.headers),
        }
