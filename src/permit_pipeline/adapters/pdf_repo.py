from ..fetcher import FetchResult

class PDFRepoAdapter:
    vendor = "pdf_repo"
    def accepts(self, result: FetchResult) -> bool:
        return result.content_type == "application/pdf"
    def extract_raw(self, result: FetchResult) -> dict:
        return {
            "source_url": result.url,
            "content_type": result.content_type,
            "text": "[PDF CONTENT ELIDED]",
            "headers": dict(result.headers),
        }
