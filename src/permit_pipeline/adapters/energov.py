from bs4 import BeautifulSoup
from ..fetcher import FetchResult
from urllib.parse import urljoin

class EnerGovAdapter:
    vendor = "energov"

    def accepts(self, result: FetchResult) -> bool:
        # Charleston's EnerGov content is served as HTML with PDF form links
        return result.content_type.startswith("text/html")

    def extract_raw(self, result: FetchResult) -> dict:
        soup = BeautifulSoup(result.body, "html.parser")
        forms = []

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.lower().endswith(".pdf"):
                form_name = link.get_text(strip=True) or "Unnamed Form"
                form_url = urljoin(result.url, href)
                forms.append({"name": form_name, "url": form_url})

        return {
            "source_url": result.url,
            "content_type": result.content_type,
            "headers": dict(result.headers),
            "forms": forms,
            "text": soup.get_text(" ", strip=True),  # keep raw text for fallback
        }
