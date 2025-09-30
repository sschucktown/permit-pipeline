from .config import CrawlConfig
from .fetcher import HttpFetcher
from .adapters.energov import EnerGovAdapter
from .extractor import to_raw_payload
from .parser import parse_fields
from .normalizer import normalize
from .dedupe import is_changed
from .review_queue import route, ReviewItem
from .db.models import PermitRecord
from .db.repo import InMemoryRepo
from .monitoring import log_event
from .utils import gen_id


def run_demo():
    # --- Config & setup ---
    cfg = CrawlConfig()
    fetcher = HttpFetcher()
    adapter = EnerGovAdapter()
    repo = InMemoryRepo()

    jurisdiction_id = "charleston-city"
    authority = "City of Charleston"
    source_url = "https://www.charleston-sc.gov/2483/Applications-Guidelines"

    # --- 1. Fetch ---
    result = fetcher.fetch(source_url)
    log_event("fetched", url=result.url, etag=result.headers.get("ETag"))

    # --- 2. Adapt -> Raw ---
    if adapter.accepts(result):
        raw_dict = adapter.extract_raw(result)
        raw = to_raw_payload(raw_dict)
    else:
        log_event("adapter_rejected", vendor="energov", url=source_url)
        return

    # --- 3. Parse ---
    parsed = parse_fields(raw.text)
    log_event("parsed", fields=parsed.fields, confidence=parsed.confidence)

    # --- 4. Normalize ---
    canonical = normalize(parsed.fields, jurisdiction_id)
    log_event("normalized", canonical=canonical)

    # --- 5. Dedupe & Routing ---
    existing = repo.get_by_local_id(source_url)
    if not existing or is_changed(canonical["change_hash"], existing.change_hash):
        decision = route(parsed.confidence, cfg.autopublish_confidence, cfg.review_confidence)
        log_event("routing", decision=decision)

        record = PermitRecord(
            permit_id=gen_id(),
            jurisdiction_id=jurisdiction_id,
            authority=authority,
            local_source_id=source_url,
            permit_type=canonical["permit_type"],
            trade_tags=canonical["trade_tags"],
            fees=canonical["fees"],
            submission_url=canonical.get("submission_url"),
            effective_date=canonical.get("effective_date"),
            change_hash=canonical["change_hash"],
            raw_payload=raw_dict,
            parsed_payload=parsed.fields,
            confidence_score=parsed.confidence,
            provenance={"headers": raw.headers},
        )

        repo.upsert(record)
        log_event("stored", permit_id=record.permit_id, decision=decision)
    else:
        log_event("no_change", local_id=source_url)

    # --- 6. Print stored permits ---
    for rec in repo.all():
        print("\n=== Canonical Permit Record ===")
        print(f"permit_id: {rec.permit_id}")
        print(f"jurisdiction_id: {rec.jurisdiction_id}")
        print(f"authority: {rec.authority}")
        print(f"type: {rec.permit_type}")
        print(f"trade_tags: {rec.trade_tags}")
        print(f"fees: {rec.fees}")
        print(f"submission_url: {rec.submission_url}")
        print(f"effective_date: {rec.effective_date}")
        print(f"confidence: {rec.confidence_score}")
        print(f"change_hash: {rec.change_hash}")


if __name__ == "__main__":
    run_demo()
