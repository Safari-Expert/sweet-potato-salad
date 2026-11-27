# Hotel source and calendar tools

| Stage | Helper | Input decision required |
| --- | --- | --- |
| Inventory and extraction | [hotel_source_cache.py](../../scripts/hotel_source_cache.py) | Authorized source root and separate cache directory |
| Calendar expansion | [hotel_intervals.py](../../scripts/hotel_intervals.py) | Source-supported seasons, event boundaries, exclusions and current-month cutoff |

Read each helper’s module documentation for its job schema. Each helper works on local files.

## 1. Inventory and cache PDF extraction

Example job:

```json
{"version":1,"root":"<authorized-source-root>","cache_dir":"<separate-cache-directory>","paths":["Property/source.pdf"],"extract_pdf":true,"mode":"plain","min_text_chars":30}
```

Omit `paths` to recursively inventory the root. Cache and report destinations must be in this client's separate local workspace, outside that root and every Google Drive/synced location; being outside only the source root is insufficient. The helper hashes current bytes, groups byte-identical files, and caches page-indexed text/annotations by source hash, parser version and extraction settings. Corrupted cache entries are rebuilt; source files are not rewritten. `pypdf` must be installed for PDF extraction; non-PDF files are inventoried only. Use the PDF skill for visual review and OCR when required. Low-text pages and extraction errors remain visible review work.

Neither matching bytes nor a cache hit proves rate validity or the suitability of a tariff for the requested property and dates. Keep source-to-property/edition decisions separately. Use a distinct cache for each client and reuse entries only for that client. Identical hashes do not permit another client's cache. This cache is private task evidence and may contain supplier text; do not bundle its contents into the skill or public outputs.

## 2. Inclusive interval mechanics

`hotel_intervals.py` accepts `version:1` and an `operation`: `union`, `clip`, `subtract`, `split` or `merge_records`. Intervals use `start_date`/`end_date` in ISO format. `clip` takes a `window`; `subtract` takes `exclusions`; `split` takes `cut_dates`, each starting a new segment. `merge_records` takes records with a complete `payload` and merges only matching payloads. Include every room, age, occupancy, board, price and source-policy discriminator in that payload.

Use decimal strings for monetary payload values. Noninteger numeric payloads are rejected so the JSON round trip cannot silently change a numeric value into text; integer, text, boolean and null payload types remain distinct.

For a holiday on one date, split at that date and the following date. One-day seasons are valid. Compute the first day of the current user-local month before supplying the clip window; no year/month is hardcoded. Review overlaps before union/compression, since set operations deliberately combine overlapping input coverage. Never use interval length alone to qualify source/catalog year tags, infer closures or choose which conflicting tariff wins.

Use Python 3.11 or newer. The extraction helper uses pypdf. The workbook and lodge PDF helper uses openpyxl and pypdf. Run the selected JSON-job helper with `python scripts/<helper>.py JOB.json --output RESULT.json`; see each command’s `--help`. For workbook output and PDF page selection use [contract file tools](../local-tools.md).
