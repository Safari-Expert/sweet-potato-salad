# Compare hotel upload times

## Measure elapsed time

When asked which workflow is faster, start one wall-clock timer **before the first property research** and stop after all requested language/media/document/tag readbacks, price checks and deliverables are complete. Include research, source access failures/fallbacks, downloads, image checks, prose/translation, model calls and review, authentication, file preparation/validation/import, coverage-tag calculation, source-PDF encoding/uploads, updates, retries and verification. Record stage timings as supporting diagnostics. Overlapping stages do not add up to total elapsed time; API-only time is not end-to-end time. Record any user/external wait explicitly and do not silently remove it from total wall time.

For a requested comparison, use the same inputs, languages, photo counts, pricing cases and completion criteria. Distinguish fresh preparation from reuse and include failed runs and retries.

Reuse valid source packets, downloads and returned media references during ordinary uploads; in a benchmark, label that reuse consistently. Cache invalidation depends on source revision, requested languages, source room mapping and tenant. Favor one property discovery pass, batched deterministic content checks, combined per-record updates and concurrent independent work. Do not sacrifice correct property identity, price validation, language coverage or cover selection for speed.
