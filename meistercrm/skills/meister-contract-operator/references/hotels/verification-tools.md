# Hotel coverage and buying-price tools

| Stage | Helper | Input decision required |
| --- | --- | --- |
| Existing-catalog reconciliation | [hotel_rate_diff.py](../../scripts/hotel_rate_diff.py) | Normalized expected/actual rows with explicitly matched identities and comparison scope |
| Representative live price checks | [hotel_price_checks.py](../../scripts/hotel_price_checks.py) | Labelled candidate cases, independent expected totals and captured responses |

Read each helper’s module documentation for its job schema. Each helper works on local files.

## 1. Compare prepared and persisted coverage

Normalize connected catalog readbacks into rows with explicit identity keys, dates, age/pax bounds, currency and monetary fields. Bind each saved room to its actual master.

`hotel_rate_diff.py` partitions the union of date, age and pax boundaries. Equivalent segmentation passes; missing, unsupported, overlapping and differently priced coverage is reported. Null differs from zero. Supply an optional `window` to restrict the audit; no automatic historical deletion follows. The cell budget bounds work, and a budget failure/empty comparison is not a pass. Detail truncation is reported without suppressing discrepancy counts.

Expected rows must come from a reviewed model. This comparison cannot certify that model against a PDF. It proposes no mutations; resolve findings through the [ID-preserving update procedure](profile-upload.md#existing-hotel-add-new-rates-with-id), retain real closures, and validate the incoming-plus-existing union before import.

## 2. Select and compare price checks

Supply candidate cases with stable IDs and reviewed feature labels. Labels can cover rooms, source-defined guest bands, boards, single occupancy, special dates and boundaries without hardcoded age/holiday assumptions. The deterministic selector covers required labels or reports uncovered features; it does not invent test expectations.

Compare captured responses with explicit expected amounts, currency and IDs. Keep `source_reviewed` expectations distinct from `serialized_rows` consistency checks. Only independently source-reviewed expectations contribute evidence of PDF-versus-system accuracy. Declare any accepted numeric tolerance explicitly with its rationale; do not hide rounding differences in an unexplained tolerance. Missing/duplicate responses and embedded errors cannot pass merely because transport returned HTTP 200. Execute requests separately through the existing authenticated pricing procedure.

Use Python 3.11 or newer. Run the selected JSON-job helper with `python scripts/<helper>.py JOB.json --output RESULT.json`; see each command’s `--help`. For workbook output and PDF page selection use contract file tools (see **Meister PDF to Contract**, Local preparation).
