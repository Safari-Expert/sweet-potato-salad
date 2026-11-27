# Reviewing a collection of supplier contracts

## 1. Inventory the collection

Identify every physical file, page, worksheet and archive member in the authorized scope. Separate unique files from identical copies. Record source-only, output-only, superseded, unreadable and unresolved items. Build a many-to-many source/output map. A directory scan or a text extraction is an inventory result. Mark a document studied only after its relevant commercial terms and examples have been checked. Resume from the last verified file and invalidate dependent results when a source or interpretation changes.

For an exhaustive review, expand nested archives within the authorized scope and identify each member by its parent. Record broken or out-of-scope shortcut targets without following them. Keep unreadable files, duplicates, empty files and removed paths in the inventory with their disposition. Record a content hash only after reading the bytes. Track files inspected, source/output pairs compared and issues resolved separately. At handoff, rescan the selected source root and reconcile changed or newly arrived files.

## 2. Pair sources and outputs

Maintain many-to-many source/output relationships. Consider the same directory, ancestor collection documents, siblings and verified duplicate sources, then match the property, room, year, market, currency and rate unit to the selected tariff.

A collection PDF can support many child folders; one output can combine successive yearly PDFs. Inspect original validity and detailed seasons before resolving year-boundary conflicts. Record source sections and common footnotes, not just a property-name search match.

Detect file encoding, delimiter and actual headers. Source files can include a legacy 21-column hotel schema missing `tax` and `ai_supplement`, Windows-1252 CSV data and DD/MM/YYYY dates. Schema age is not automatically an error; normalize only in private comparison work and use the selected current template for newly generated output. Never interpret a missing legacy field as an included zero-cost option.

## 3. Study every relevant unit

For each package in the customer-authorized collection:

1. Read all source pages, sheets, tables and conditions. Render and visually inspect PDFs at legible resolution; OCR scanned text and verify it against pixels. Read hidden sheets, formulas/cached values and notes. Importing the first worksheet is not whole-workbook study.
2. Identify STO versus RACK throughout the source. Use only explicitly supported STO amounts/derivations, or annotate the user's assumed-STO convention when no retail rate is present. Record exclusions and unresolved RACK-only input.
3. Verify the selected tariff's table, property, dates and commercial terms against the source.
4. Read every curated data row, preserving zeros, blanks, headers and row locators. Extract a matrix of rooms, capacities, ages, seasons, meal plans, prices, currency, taxes, mandatory extras and unsupported conditions.
5. Build an independent expected representation and compare in both directions: incorrect/unsupported output rows and omitted source terms. Reconstruct room totals and all supported occupancy combinations, not just field values.
6. Record compact findings with source page/table or sheet/cell, output row range, calculation, decision and evidence. Group repeated identical findings by affected scope; do not write a narrative for every row.

Classify confirmed mistakes, accepted user modelling simplifications, schema evolution, importer limitations, ambiguous source and missing evidence separately. Human curation is a teacher to investigate, not unquestionable ground truth. Source-only and output-only files remain studied to the available extent, with comparison blocked where evidence is missing.

## 4. Check commercial coverage

Use this checklist alongside the detailed pricing rules.

| Topic | Required checks |
| --- | --- |
| Commercial basis | STO only; exclude RACK; distinguish assumed versus explicit STO and supported discount derivations |
| Occupancy and ages | Per-room division; [current min_pax 1 default and scoped overrides](occupancy-and-ages.md#room-names-and-occupancy-decisions); max_pax equal capacity; supplier-derived age bands and verified room aliases |
| Missing places | [Adult-cost base and quoted Single override](occupancy-and-ages.md#current-output-rule-adult-cost-supplement-8-october-2026), then [country adjustments and monetary rounding](../hotels.md#vat-country-adjustments-and-rounding); all supported partial/full occupancy totals |
| Children and infants | [Child policy](child-policy.md): supported discounts; quoted one-adult sharing tariff before an adult fallback for unrepresentable sharing conditions; infant zero conventions and physical/priced capacity distinction |
| Meal plans | Baseline cost label; independent HB/FB/AI increments; unavailable blank versus included zero; inclusive-only packages |
| Seasons and extras | Exact validity, year boundaries, holidays, mandatory meals and closures; do not fabricate dates or availability |
| Precision and compatibility | Original units, division residuals, supplement precision, older schemas, valid one-day seasons versus checker restrictions and importer limits |
| Mixed products and eligibility | Nightly rooms versus duration-priced packages; separate schedules for different markets; component-specific refund deductions, credit restrictions and deadline anchors |

Use [occupancy](occupancy-and-ages.md), [child policy](child-policy.md), [dates and seasons](dates-and-seasons.md), [meal plans](meal-plans.md), [commercial evidence](commercial-and-signatures.md) and shared [checking gates](../general/checking-gates.md). Keep unsupported booking/stay/composition conditions and pricing consequences explicit.

## 5. Review findings independently

Review boundary cases against supplier pages before looking at the prepared answer. Keep shared collection documents and related editions together when assigning work. Record pages, rows and cases actually examined. A pilot estimates the remaining effort. It does not establish coverage of unseen properties. Generalize a finding only when it changes a future decision, and retain the supplier-specific scope in private evidence.

For an independent evaluation, hold out complete supplier families with related editions together. Generate expected rates independently and compare source-derived amounts and held cases before reconciling the results.

## 6. Tests and completion

Test observable outcomes, not whether the documentation contains particular words:

- All double/triple occupancies; adult/child/infant combinations; age boundaries and unsupported-sharing fallback.
- Null/zero/positive board options, independent increments, inclusive-only plans and free/equal-price upgrades.
- STO/RACK side-by-side tables, unlabeled assumed STO, RACK-only rejection and supported STO derivation.
- Seasonal gaps, closures, year boundaries, one-day holiday restrictions and recurring-decimal precision.
- Legacy headers, non-UTF-8 CSVs, multi-sheet/formula workbooks and source version relationships.
- Inventory/tree count reconciliation, state-preserving resume, changed-source invalidation, dependency invalidation, incomplete-coverage rejection, and archive expansion.
