# Flight contract updates and checks

Use the connected customer catalog to amend or verify an existing flight.

Keep these identities distinct:

- Airline master ID selects the parent.
- Contract ID identifies the exact existing rate to amend.
- Compare departure options separately for each directional route.

## Update and complete readback

1. Fetch every contract for each authorized airline. Retain a private baseline keyed by `contract_id`, with parent/tenant identity, routes, clock times, weekdays, ages, dates, costs and pax bounds. A filtered or paged UI view does not establish full coverage.
2. Match the baseline to the approved amendment and any in-scope canonical workbook/CSV. Normalize display-only number/date formatting for comparison; preserve currency, units, zero and null meanings. Investigate count, identity or price differences before writing. Recheck overlapping coverage after applying the pax convention.
3. For a pax-only amendment skip rows already at 1–99. Send the affected fields for the matched contract through its supported MCP update tool.

4. Read back the first corrected contract and then check remaining updates.
5. After an uncertain outcome, re-read the affected contracts and reconcile before retrying.
6. Fetch the full lists again after completion. Require unchanged contract-ID sets and counts per parent, correct tenant/parent binding, and **1–99 on every contract**, including zero-price age rows. Compare every other business field with the baseline; server-managed audit fields such as `updated_at`/`last_updated_by` may change. Reconcile any in-scope saved workbook and requested CSVs to the persisted route/time/weekday/age/date/pax/cost rows.

Preserving existing contract IDs avoids breaking references.

## Source PDFs when creating contracts

Every authorized flight-contract creation/import must complete [required source PDF attachments](live-updates-and-checks.md#required-source-pdf-attachments) on the intended airline record, including relevant tariff and surcharge/amendment PDFs. Preserve existing documents during amendments. Verify the saved attachment filenames through airline readback; rate persistence and document attachment are separate completion checks. This guidance does not change the scope of a pax-only correction or authorize a live upload merely because the skill was edited.

## Buying-price checks

Generate unique synthetic traveler IDs and ISO dates of birth. Age eligibility comes from the effective contract bands and test date; the 1–99 pax convention does not establish those bands or a free infant fare. Use the requested source NET/STO fare and any explicit user age convention. Do not import a package discount into one-way fares or add YQ again when the selected NET already includes it.

Check an appropriate matrix for the changed scope:

- One adult; two adults; one adult plus one child; two adults plus one child; two adults plus two children. Add infants when their fare is supported and confirm the zero or paid contribution explicitly.
- The actual inclusive age boundaries and any unpriced ages; dates in each relevant validity/year/season; each distinct departure/fare product under test.
- Under the standing pax convention, one and 99 eligible travelers should price; 100 adults should return a pax rejection. Source-minimum negative tests expecting two/four seats are superseded by 1–99. Check dates outside validity as negative cases too.

Compare the actual buying price for each departure and traveler against independently reconstructed fares in the quoted currency. Check FX and tax separately from customer totals and markup. Keep the airline’s markup unchanged when checking buying prices.

A valid case needs the expected group, selected contract(s), correct total/unit costs and no pricing errors. A zero total alone does not establish a free fare. For negative cases require the relevant error, such as `age_not_covered`, `pax_not_covered` or `date_not_covered`; rejected items can have `contract: null`. Preserve raw errors in private evidence rather than labeling rejected/partial pricing as a successful free quote.

Record cases/options checked, expected versus actual amounts, expected rejections and any untested scope. Reopen any delivered files and complete the full persisted-row checks before reporting completion.
## Required source PDF attachments

Every authorized creation/import of flight contracts in MeisterCRM includes attaching the actual supplier source PDF document(s) to the intended client's airline record in the system. This also applies when adding new rate contracts under an existing airline. A Drive link, prepared XLSX or local file alone does not satisfy this requirement. Include every source PDF used for the created rates, including applicable tariff editions and separate fuel-surcharge notices or amendments.

Attach original supplier PDFs through the supported MCP attachment tool. Preserve source filenames, current attachments and contract IDs.

After saving, read back the airline and match the expected source PDFs. Report missing attachments separately from saved rate rows.

## Rechecking a sample or amending a fare

Inspect the actual header, including `tax`, before using an older export. Sample schedules and synthetic fares cannot establish operating days, departure times or a supplier price. For adjacent source bands such as infant 0–2 and child 2–11, establish who pays which fare at age two before creating inclusive rows. Confirm the arrival day separately for an overnight sector whose two local clock times leave it unclear.

For a requested year-only edit, preserve every other field and identify the evidence for renewed validity. Match amendments by the saved contract IDs, read back the complete affected scope and use [flight price checks](live-updates-and-checks.md) for supported departures and boundary rejections. Deliver the actual maintained workbook (see **Meister PDF to Contract**, Source documents to prepared rate workbooks) and check the supplier PDF attachments.
