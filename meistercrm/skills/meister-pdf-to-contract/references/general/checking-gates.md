# Checking gates for contract delivery

For hotels, apply the [approved source-normalization decisions](../hotels/workflow.md#decision-order) before these saved-output checks. Record printed facts and normalized values separately. An accepted calendar or age repair must produce real dates and disjoint applicable bands; it is not permission to waive invalid dates, overlaps or unknown prices in the emitted file. Local interval helpers and validators consume the reviewed normalized values rather than silently rewriting source evidence.

## Record the decision, not just the error count

For each finding, record the file, raw check/error code, row(s), product identity, affected dates/age/pax bands, source locator, decision, and reason in task notes or a separate validation report. Never add these fields to the import CSV. Use these outcomes:

- **Pass:** the check ran and its invariant holds.
- **Fix required:** malformed data, unsupported values, conflicting prices/identity, duplicates, capacity/currency conflicts, or demonstrated extraction loss. Correct from evidence and rerun.
- **Review required:** source coverage or interpretation is unresolved. Resolve only the affected scope; do not guess a price, eligible age, or closure.
- **Accepted source exception:** a specific source or explicit user instruction supports the flagged absence or statistical anomaly. Preserve the correct source data and retain the finding and evidence. This can complete file preparation even when the import validator still reports failure.
- **Accepted user convention:** a confirmed domain rule applies despite a checker mismatch; follow its exact scope, such as [valid one-day hotel seasons](../hotels/dates-and-seasons.md#valid-single-day-seasons). Retain the raw result without treating the approved data as invalid or blocking its delivery.
- **Not checked:** the needed reference, current configuration, or existing target data was unavailable. State that limit without manufacturing a pass.

Report conversion integrity separately from import acceptance. A skipped check or successful transport alone cannot establish validated prices.

Preserve valid source-supported closures and one-day hotel intervals. Document any tool rejection and hold affected writes until the supported interface accepts them.

## Gates in correction order

| Gate | Check and outcome  |
| --- | ---  |
| 1. File and schema | Reopen saved bytes; exact selected headers/order, consistent row width, no empty data set or helper/error columns, valid quoting/encoding. Apply upload/cell limits before claiming import compatibility.  |
| 2. Required values and identity | Required fields and allowed/forbidden field combinations for the selected type; exact reference matching; target names for a scoped import. Fix identity before interpreting group errors.  |
| 3. Values and units | Numeric parse, finite amounts, integer eligibility/capacity, nonnegative costs, margin/tax fractions 0–1, age 0–999, ordered pax/ages, ordered dates (hotel start may equal end under the [one-day season rule](../hotels/dates-and-seasons.md#valid-single-day-seasons)), domain capacity/boolean/type rules. Reconcile source units and blank versus zero too.  |
| 4. Master consistency | Raw currency agrees within its owning scope and with an existing target; stable capacity and first-row master metadata. Do not silently use a later row's conflicting description, subtitle, tax, or feature set.  |
| 5. Duplicates and conflicting coverage | Compare all fields after outer whitespace trimming; then compare date/age/pax coverage within the actual group key. Genuine duplicates/conflicts need correction, not a seasonal-closure exception.  |
| 6. Coverage and exceptions | Reconcile source validity, products, seasons, ages and pax against output. Classify internal date gaps, eligibility gaps, missing reverse routes and statistical room outliers using source evidence. Apply the closure procedure below.  |
| 7. Existing-target and delivery | For an existing-item import, validate new plus existing contracts and target identity/currency. Keep uploaded versus existing row provenance. Reopen the final workbook, rerun affected gates, and deliver with accepted exceptions and unchecked scope stated.  |

## Date gaps: closure versus missing extraction

Reconstruct the supplier price and eligibility across every affected date, including offers whose boundaries fall inside an output period. Matching the first day of each CSV period does not prove the rest of that period: a single-room waiver, event replacement or mobile-camp season can change later. Report numeric mismatches, missing output, output outside supplier validity, closures and unquoted interpretations separately. Preserve room-contract years independently from dates of ancillary festive meals.

A `date_gap` finding identifies a possible hole between successive seasons **within one group and an identical min/max age and min/max pax band**. Inclusive seasons are adjacent only when the next start equals the previous end plus one day. The skill's offline report uses `season_gap` and gives the missing interval, group, bands and neighboring rows.

1. Compute the missing interval and identify exactly which supplier/product/room/route, year, age and pax band it affects. Check both bordering source rows and footnotes; also inspect omitted source pages or room categories.
2. If the supplier document or an explicit user instruction establishes closure/non-operation for that interval and scope, classify it as an **accepted source exception**. No further confirmation is needed when the evidence is already explicit. Preserve the two open periods; create no closed-period contract rows and never bridge the gap with zero, copied, interpolated or invented prices.
3. Verify the closure covers the whole flagged gap. Evidence for April does not explain missing May, another year, a different room, route or supplier. Do not apply a whole-hotel closure to an independently operating product unless supported. A valid closure for one band does not conceal a missing child rate during an open season.
4. If closure is only plausible, leave **review required**. Investigate the source or ask the missing narrow question. Rainy season, destination, low-season labels, or absence of a price alone do not establish closure.
5. Retain the raw finding and its source-backed exception. Validate proposed additions against the existing hotel’s rates through MCP. Report a rejected import and hold the affected rows. A documented closure can explain a validation finding without authorizing a write.

Example, not a destination default: a supplier explicitly closes a hotel from 01/04/2027 through 30/04/2027. Valid rates ending 31/03/2027 and restarting 01/05/2027 must retain the April gap. A Zanzibar hotel is not presumed closed simply because another supplier closes in April. This rule applies to all contract types when an actual non-operation period is supported.

## Completion gate

Deliver a concise record such as: “Structural/value checks passed; one documented seasonal closure accepted; no unresolved extraction findings; connected import acceptance not checked,” or “Source-exact CSV complete with one accepted closure; IO validation reports `date_gap`; not imported.” Say **validation passed** only after running the relevant enabled checks and inspecting the result. Say **import accepted/persisted** only from the actual write response and persisted-row verification; that outcome can coexist with a separately documented accepted seasonal gap. Never present an accepted exception as an unqualified zero-error validation run.

## Independent checks when a validation result looks clean

- Resolve overlaps before interpreting gaps. Check inclusive date and age intersections for equal **and intersecting but unequal** pax bands. An enclosing interval can eliminate an apparent hole. Merge covered intervals first, and still report conflicting prices separately.
- For each age and pax pair, compare coverage with the requested source validity, including missing first and final seasons. For each individual pax tier, verify all eligible ages. A child row in another tier cannot prove coverage here. Check permitted group sizes separately. An explicit admission minimum can legitimately exclude younger guests.
- Fix invalid dates, ages and missing identity first, then rerun. Independently verify daily transfer intervals with blank routes. Normalize case and whitespace to discover candidate aliases, then compare the raw name and catalog identity. Check add-on scope and charging basis before matching.
- A room-count outlier can mean a misspelling, seasonal room, renovation, new category or narrower eligibility. Diagnose it against the source. Preserve genuine differences in row counts.
- Use finite monetary values, unambiguous dates, canonical booleans, verified currency codes, integral ages/pax, valid local flight times and explicit weekdays. A parser accepting a value does not establish its meaning.
- Read all related rows and underlying findings. A displayed row error can mask a second error. Rerun after each correction. Validate existing and incoming contracts together for the actual target.
- Inspect the connected tool’s current file limits before staging. The offline preflight defaults are hotel 8 MiB/1,000 rows, flight 5 MiB/3,000 rows, other families 2 MiB/1,000 rows, and 30 columns. If a coherent batch must be split for transport, reconcile the combined product, currency and coverage matrix and maintain one customer workbook.
