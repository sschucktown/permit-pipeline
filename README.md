<<<<<<< HEAD
# permit-pipeline
=======
# Permit Pipeline – Step 1 Skeleton (Architecture Scaffold)

This is the **Step 1** scaffold for the high‑level architecture of the PermitGet crawler/canonicalizer, optimized for **data accuracy & integrity** with a human‑in‑the‑loop (HITL) path.

## Modules

- `fetcher.py` — Polite fetcher interface (HTTP/PDF/API), supports vendor hinting & rate limiting.
- `adapters/` — Vendor/portal adapters: `base.py`, stubs for `energov.py`, `tyler.py`, `pdf_repo.py`.
- `extractor.py` — Converts fetched resources (HTML/PDF/raw JSON) into a normalized `RawPayload`.
- `parser.py` — Hybrid rules/ML placeholder extracting fields into `ParsedPayload` with confidences.
- `normalizer.py` — Canonical mapping to your schema, unit/date/currency normalization.
- `dedupe.py` — Change detection and deduping via `change_hash` for key fields.
- `review_queue.py` — Human‑in‑the‑loop routing stubs (approve/reject/edit).
- `db/` — Persistence: schema draft (`schema.sql`) and a minimal repo (`repo.py`) with append‑only revisions.
- `monitoring.py` — Telemetry stubs and KPI placeholders (precision/recall, change latency).
- `main.py` — End‑to‑end orchestration demo over a mock Charleston seed without network calls.

## Quick start

```bash
python -m permit_pipeline.main
```

You should see a simulated run that flows: **Fetcher → Adapter → Extractor → Parser → Normalizer → Dedupe → ReviewQueue → DB** and prints the staged artifacts with confidences and routing decisions.
>>>>>>> 5795dc8 (Initial commit: Permit Pipeline Step 1 scaffold)
