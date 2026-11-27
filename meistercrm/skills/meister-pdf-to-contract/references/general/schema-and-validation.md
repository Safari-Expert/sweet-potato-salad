# Shared schema and validation

Use [checking gates](checking-gates.md) to classify findings, handle documented closures, and distinguish CSV integrity from connected import acceptance. The following is the data contract; the gates define when a finding needs correction, review, or an evidence-backed exception.

## Resolve evidence by the decision it answers

Apply [rule ownership and precedence](rule-ownership.md). For formatting, use the current task template with explicit hotel representation overrides, then the connected tool’s template. For commercial meaning, use explicit user scope and current supplier/authority evidence. For import acceptance, validate the workbook through the connected tool against the existing target. The handbook and history explain intent and corrections; an old assistant answer alone does not establish a fact.

If the current template and importer disagree, preserve the conflict and resolve the affected rows. Do not silently strip columns, invent fields, or copy a known defective implementation as a business rule. Follow the [rule precedence](rule-ownership.md) when resolving conflicts.

## Headers and representation

| Type | Columns in supplied sample | Key representation |
| --- | ---: | --- |
| Activity | 17 | `group_flg` distinguishes person and group costs |
| Flight | 18 | `frequency` is a quoted comma list; source sample has no trailing comma |
| Transfer | 16 | `daily` has empty route cells; `taxi` has both endpoints |
| Location | 12 | Main `cost`, additive `overnight` and `camping`; no CSV pax fields |
| Hotel | 23 | Hotel -> room -> contract; four supplement columns |
| Add-on | 24 | Add-on identity/subtype/features plus price type |

Common output conventions: dates follow the selected template, with `DD/MM/YYYY` retained for the older non-hotel templates; current hotel outputs use the explicit representation below. Keep ordered start/end, with hotel `start_date == end_date` accepted as a [valid inclusive one-day season](../hotels/dates-and-seasons.md#valid-single-day-seasons); uppercase `TRUE`/`FALSE`; numeric values without symbols or thousands separators; no exact duplicate rows; blank optional fields stay empty. Numeric rates/costs must be finite. Numeric-looking IDs are identifiers, not numbers to reformat. Boolean and frequency formatting follow the selected template except where the explicit hotel rule applies.

### Current hotel output representation

The user's general correction of 8 October 2026 overrides older hotel samples in these specific respects:

- Always include all three board columns in this order: `hb_supplement`, `fb_supplement`, `ai_supplement`, including when a legacy template omitted any of them. Keep each header even when that board option is unavailable, leaving its cells genuinely blank/null. Use a supported amount, or numeric zero when that option is included or explicitly free for the guest. An unquoted price remains an evidence gap, not proof that the supplier does not offer the option. Preserve the other selected columns and their order. This does not require adding an absent `tax` column.
- Store `inside_restricted_area` and `ignore_proposal_margin` as literal text `FALSE` under this user workflow, unless the user explicitly selects a different value. Address fields by header name, not spreadsheet letter. Use uppercase text, not typed spreadsheet booleans or checkbox cells; do not silently retain a conflicting legacy `TRUE` against the user's default.
- Render hotel dates as `YYYY-MM-DD` (`yyyy-mm-dd` for Excel number formatting) and serialize that same calendar date in CSV. In XLSX, write numeric Excel date serials under the workbook's date system (`t="n"`) with that number format, then reopen the exported cells and check values and displayed dates without a timezone day shift. Do not rely on a preview or an OOXML `t="d"` date alone for spreadsheet round-trip compatibility. Verify the date again after the customer’s spreadsheet app saves a copy. Older `DD/MM/YYYY` hotel examples are historical.
- Applicable supplements that are zero must be numeric zero displayed as `0`, not `0.00`. Keep unavailable options blank/null. Preserve intermediate calculation precision, then apply the [final two-decimal monetary rounding](../hotels.md#vat-country-adjustments-and-rounding) convention. Zero display uses number formatting; keep monetary cells numeric rather than replacing them with text.

Verify saved headers, cell types, date values/formats, zero displays and blank-versus-zero board availability independently. The [current adult-cost supplement rule](../hotels/occupancy-and-ages.md#current-output-rule-adult-cost-supplement-8-october-2026) determines `single_supplement` values; these representation rules do not change the importer or authorize live import.

The preparation defaults set `margin=0` and `ignore_proposal_margin=FALSE` as business defaults for activities, flights, and transfers unless instructed otherwise. These settings can fill missing source fields, with their business-default provenance retained. They do not establish a tax rate or currency, and an example-only zero in a hotel/add-on workbook is not by itself a new business default.

### Calculation precision and saved XLSX formulas

Preserve calculation precision when copying the adult amount, including recurring whole-room divisions under [occupancy and ages](../hotels/occupancy-and-ages.md#establish-units-and-room-identity). Reconstruct the room total before final [country adjustments and two-decimal monetary rounding](../hotels.md#vat-country-adjustments-and-rounding). A zero displayed as `0` instead of `0.00` is a formatting choice. Apply [hotel output representation](schema-and-validation.md#current-hotel-output-representation): numeric Excel dates displayed `YYYY-MM-DD`; literal text `FALSE` for both `inside_restricted_area` and `ignore_proposal_margin`, without checkbox cells; and all three columns `hb_supplement`, `fb_supplement`, `ai_supplement` always present, with unavailable options blank/null. That reference owns serialization details; saved monetary precision and actual acceptance remain separately checked.

#### Saved XLSX formulas must survive reopening

Correct cached prices can coexist with stale shared-formula metadata from an imported workbook. The visible formula text alone can also mislead: spreadsheet readers may derive the effective formula from a shared anchor and override that text.

After revising source calculations, reopen and independently evaluate effective formulas. Compare with cached values and approved expected prices. If the saved file still applies an inherited shared formula, repair the affected formula group or rebuild that part of a working copy. Preserve the intended formulas, reviewed values and meaningful layout. Verify the effective formulas and recalculated results after reopening. Store literal payable values on `Contracts` and retain evidence on `Original`.

## Identity and grouping

Master identity, currency scope, and overlap grouping are different questions. Validate each separately.

| Type | Currency scope | Current overlap/continuity group |
| --- | --- | --- |
| Activity | location + activity name | location + activity name |
| Flight | airline name | airline + origin + destination + departure + arrival |
| Transfer | vehicle name | vehicle + origin + destination + type |
| Hotel | location + hotel, across rooms | location + hotel + room |
| Add-on | name + add-on type + price type | **name only** in current validator |
| Location | location, including existing contracts | location + contract type; group rows also include description |

Source currencies remain raw catalog currencies, uppercase three-letter codes. Non-location currency belongs to the master; location currency travels on each contract. Existing-item imports must agree with the existing master/location and validate the union of new and existing rows. A globally mixed-currency file is fine only across distinct valid currency scopes. Do not split a master by currency unless explicitly modelling distinct products with user agreement.

## Ranges and coverage

- `0 <= margin <= 1`; nonnegative finite costs/supplements; integral nonnegative ages/pax/capacity.
- `0 <= min_age <= max_age <= 999`, and `min_pax <= max_pax`.
- Activity/transfer capacity is at least max pax; transfer capacity is consistent per vehicle. Hotel booking minimum and capacity are positive; max pax equals room capacity and remains consistent per room. Source-specific booking minima still require evidence; a bed count alone does not establish them.
- Check every intersection of dates, ages and pax in the applicable product, including unequal intersecting pax bands. Reconcile overlaps against source eligibility.
- Check expected age coverage separately for each pax band; a band in another group size must not hide a missing child row. Begin at the actual participation age, not automatically zero.
- Adjacent inclusive seasons end one day before the next starts. A documented closure is an accepted source exception, not missing rate data. Follow the exact-scope closure procedure in checking gates; preserve the gap and separately report any connected import rejection.

## Validation tools

Run the packaged offline check after producing a file:

```text
python scripts/validate_contract_csv.py --type flight --template <current-flight-template.csv> --location-ref <fresh-task-location-reference.json> <output.csv>
```

The optional local preflight reads a CSV or XLSX template and a temporary CSV serialization of `Contracts`. For location checks supply a local JSON list of authorized catalog references. Keep that diagnostic serialization outside the delivered folder.

The script checks formatting, effective selected columns, row shape, offline preflight size limits, finite/integral numbers, domain basics, exact location names, currency consistency, trimmed duplicates and same-pax overlaps. For hotels it normalizes the template's board-header block to include HB/FB/AI in that order, preserves other selected columns, and requires the flags and Single supplement header. It checks ISO dates, inclusive one-day intervals, literal FALSE flags, supplied tax zero, final money with at most two fractional digits, and supplement zeros serialized as `0`. An actual room-name collision under case/whitespace normalization fails for identity review; it does not rename or merge rooms. Existing target aliases must still be inspected separately.

It reports scoped date/age gaps, intersecting unequal pax bands, room-count outliers, master spelling/metadata drift, and reverse-route coverage as review items. It cannot know source truth, supplier eligibility, missing products, current catalog contents, every importer constraint, or actual deployment behavior. A passing result is **offline checks passed**, never “production import validated.”

An explicit task instruction may override a hotel flag default using `--hotel-flag-policy <json>`. The object permits only `inside_restricted_area` and/or `ignore_proposal_margin`, each with `{"value":"TRUE","reason":"explicit user instruction locator"}` (or FALSE). Do not create this evidence from a legacy TRUE cell or use it to waive tax/price/date checks. This option applies only to hotels; no policy file means both flags remain FALSE.

Exit codes: `0` checks passed, `1` validation errors, `2` review findings, `3` unreadable/invalid inputs or missing extraction dependency. Resolve review findings using checking gates. The script does not read supplier evidence or suppress accepted exceptions: a legitimate documented closure can keep exit 2 while file preparation is complete with a separate exception record. Do not describe that as a clean checker pass or guaranteed import acceptance. Unknown add-on price types and meaningful location tax that would be discarded are also review items. Never rewrite source values just to reach exit 0.

### Source-reviewed hotel policy check

After structural preflight, use [validate_hotel_policy.py](../../scripts/validate_hotel_policy.py) to check the current Single, free-row and AI-only conventions against grounded decisions. Prepare its private manifest from the independently reviewed source ledger, not by copying output prices to make a test pass. Adult/child roles, a quoted Single and an AI-only package are source decisions; the script deliberately does not infer them from age 99, room names or blank boards.

```text
python scripts/validate_hotel_policy.py <output.csv> --policy <source-reviewed-policy.json> --report <policy-result.json>
```

The manifest has exactly `version: 1`, `csv_sha256` for the final saved CSV bytes, and `rows`. Bind every nonblank CSV record exactly once using its logical record number (header = 1), not physical text lines. Each decision contains:

| Field | Meaning |
| --- | --- |
| `row` | Integer CSV record number |
| `role` | `adult`, `paying_child`, `paying_guest` or `free`, established from source/approved policy |
| `quoted_single` | Boolean: explicitly supported fully priced capacity-one Single product |
| `ai_only` | Boolean: source/approved policy establishes only an AI package |
| `expected_cost` | Decimal string for the independently derived final cost, including applicable fees/rounding |
| `evidence` | Nonblank source page/table and applicable rule/answer locator |
| `adult_row` | Required for paying non-quoted-Single rows; an `adult` row must reference itself; a paying child/guest references its grounded adult basis |

The adult basis must match hotel/location/room/currency/pax/capacity and cover the entire affected row interval. A constant adult tariff may cover a narrower child interval; a partial or cross-season reference cannot establish its adult basis. The check compares paying rows' supplement with that adult cost, quoted capacity-one Singles with zero supplement, free rows with zero cost/applicable supplements, and AI-only rows with blank HB/FB plus AI `0`. It compares cost to the independently reviewed expected cost and verifies full exact-file manifest coverage. It does not prove the PDF interpretation, optional meal amount, admission conditions, TDL inclusion evidence, current-month cutoff or supplier party fidelity; keep those checks in the source ledger and live price procedure (see **Meister Contract Operator**, Hotel profile upload).

Omitting `--policy` returns review with `source_policy_checked: false`. Both validators return 0 for pass, 1 for failed consistency, 2 for review and 3 for input errors. A policy pass still requires structural preflight, reopening the saved XLSX and checking its source. Follow the completion gates (see **Meister Contract Operator**, Hotel batch completion gates) for catalog work.

## Lossy or ambiguous input

Common input limits are 500 characters for text, 50 for numeric-looking cells, 380 for activity/hotel descriptions and 480 for room descriptions. Check the current connected schema. Preserve meaningful restrictions when editing for length. Reject fractional ages and pax or malformed weekdays before import. Verify fractional overnight/camping fees in the saved catalog against the exact supplier amount. If the target cannot retain a valid fraction, hold that price and explain the difference. Daily transfers need their own overlap check with both endpoints empty. A structural add-on example with blank currency or subtitle does not establish a usable commercial row.
