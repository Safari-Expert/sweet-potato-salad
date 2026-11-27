# Flight contracts

Use for supplier schedules and fare sheets. Read [shared schema](../general/schema-and-validation.md), [source extraction](../general/source-etl.md) and flight amendments and price checks (see **Meister Contract Operator**, Flight contract updates and checks).

## Row model and extraction

A row is one airline, directional sector, departure/arrival pair, age band, validity band, and passenger band. Build an extraction ledger from the supplier source before expanding rows: page/table, sector, operating days, departure, arrival, fare basis, fare currency, ages, net fare, minimum seats, capacity, validity, closures, and footnotes. Retain raw source seat conditions separately from the current 1–99 pax convention below.

- Preserve each real scheduled departure as its own rule. Do not turn a printed network connection into every possible pair of airstrips.
- Generate a return sector only when source evidence establishes its schedule and fare. The transfer reverse-route convention does not apply to flights.
- Resolve each endpoint through [live location references](../location-reference/live-reference.md). Existing destinations are valid for approved endpoint mappings; a dedicated airstrip type is not required. Group labels need supported members or an explicit approved destination mapping; do not create composite names, invent member routes or substitute a nearby airport.
- Read table footnotes before expansion. Seasonal closures and weekday restrictions can alter availability even when price is unchanged. Retain supplier inducement conditions in the ledger while applying the current pax convention below.
- Prefer the supplier net/STO/DMC column required by the contract to rack prices. A column called `FARE` is not automatically a net fare for every supplier; establish its meaning from the source.
- When a tariff has base/gross, `YQ` and NET columns, check its printed arithmetic or inclusion clause. If NET already includes YQ, copy NET unchanged; adding YQ again double-counts the surcharge. The label alone does not prove inclusion for another tariff. Keep package child discounts separate from one-way age policies.

## Dynamic fares and fixed seasonal exceptions

Exclude fares labelled **Dynamic** from the fixed contract scope by default. Retain their source rows and exclusion reason in preparation evidence, but do not create a supplier-price blocker or request a fixed quote merely because the fare is Dynamic. Do not generate a zero price, estimate or placeholder contract for an excluded fare.

If supplier evidence establishes an actual fixed fare for a defined season, create that fixed fare only between its supported start and end dates. Use its applicable route, age and other conditions; leave the remaining Dynamic periods excluded. A price without a supported period, or a season label without a fixed amount, does not justify invented rates or dates.

If a blocker was solely about Dynamic fares, record the exclusion and preserve any human reply. Assess readiness for independently supported fixed fares.

## Schema and identity

Use all columns of the selected flight template, including `tax`. Keep airline-level currency, margin, tax and proposal-margin flags consistent.

Compare potentially competing fares by airline, directional endpoints and local departure/arrival times. Verify weekdays and fare conditions independently.

## Schedule encoding

- Weekdays are comma-separated integers: Monday `1` through Sunday `7`. Daily is `1,2,3,4,5,6,7`. The CSV writer must quote that cell because it contains commas.
- The supplied workbook uses no trailing comma. Preserve the actual chosen template style; the older handbook's assertion that this sample has a trailing comma is incorrect for this file.
- Validate weekday tokens locally: use 1 through 7 with no duplicates or missing days.
- Times are 24-hour `H:MM` or `HH:MM`, with no AM/PM or timezone suffix. Normalize equivalent times consistently within the dataset so `8:00` and `08:00` do not accidentally split validation groups.
- For overnight or timezone-crossing flights, keep the supplier's local clock times and surface the day-offset question. The template has no day-offset field. Verify the intended arrival day in an actual quote.

## Ages, inducement, and availability

Translate the actual fare policy to inclusive, non-overlapping integer bands. For example, if infant includes age 2, a paid child band must start at 3; if child starts at 2, infant must end at 1. Do not repair an ambiguous supplier policy by choosing a boundary without evidence. Do not impose one historical infant/child/adult split on all airlines.

Include a zero-price infant row when supported by the fare policy or a current explicit business rule. Create child fares when published; do not manufacture a child discount. A single paid fare can be one paid age band when the source supports that policy. The sample includes `0–2`, `3–99`, and `0–99` rows; those are examples, not universal cutoffs.

### Current flight pax convention

Set **`min_pax = 1` and `max_pax = 99` for every flight rate row and corresponding authorized live contract**, including paid and zero-price age bands, all departures and all validity periods. This is the user's standing flight convention, confirmed 26 October 2026. A later explicit instruction can override it for its stated scope.

This supersedes the older guidance that copied supplier inducement minima or aircraft capacity into these two fields. Preserve printed minimum seats and aircraft capacity in the extraction ledger/route conditions, clearly distinguish them from the applied 1–99 model, and do not multiply the per-person fare by a supplier minimum. The value `99` is a contract-model convention, not a statement of physical aircraft capacity. Pax bounds do not establish infant eligibility, a free fare or a child discount.

After normalization, recheck date/age/pax coverage: if formerly distinct tiers become conflicting rules at 1–99, resolve the affected pricing model rather than choose a fare or silently drop a row.

Split rows whenever fare, age logic or operating season changes. Preserve real closure gaps and supplier validity; source seat conditions remain documented even when they do not change the normalized pax fields. A requested year-only edit should preserve the intended month/day boundaries and recheck leap days and cross-year ranges; distinguish moving a season from extending its end date.

## Final domain review

Reconcile source departures against output by route, time, weekday, age and season, retain inducement evidence in the ledger, and assert that every emitted row has pax bounds 1–99 under the current convention. Count Dynamic exclusions separately from unresolved fixed-fare work, and explain exclusions and unresolved mappings outside the clean import scope. Check that no return sector was inferred, no source footnote vanished, no tax was added twice, no weekday token was dropped, and no two active rules ambiguously price the same traveler/party. For real imports, require supplier-backed fares and validity; explicitly requested dummy datasets must remain labeled as synthetic in the delivery and provenance.

Check equivalent time spellings, weekdays, master currency and real non-operation dates. Keep a source-supported weekday distinction explicit and review a rejected one-day flight as written.
