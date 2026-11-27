# Hotel batch completion gates

Use this reference at intake and final handoff for every authorized hotel upload, import and update, including existing-record corrections and rate top-ups. It owns upload evidence, scope exceptions and completion claims. The [profile upload procedure](profile-upload.md) owns actions and payloads; onboarding (see **Meister PDF to Contract**, Hotel source intake) owns client inventory and stage selection. These gates do not replace source interpretation, authorize writes or add a cleanup requirement.

## Mandatory gate review for every upload and update

1. Freeze the selected hotel and room inventory. Review identity, languages, pictures, PDFs, coverage tags, pricing notes, saved rates, live prices and final files.
2. Determine exclusions from actual user instructions, never from an agent's description of its own work. “Import the latest rates”, “update contracts”, “add a year” or “do it fast” does not mean “rates only”. An explicit instruction such as “only change the rates; leave the profile untouched” does. Record the limiting instruction, source locator and exact subjects before excluding checks. A prior unrelated exception is not transferable. Missing companion tools, time, media or supplier evidence leaves an applicable gate pending; it does not narrow scope.
3. For existing records, inspect completeness and preserve correct IDs/content. Already verified, unchanged work may be reused with the comparison evidence below; do not re-upload images or rewrite translations merely to perform an update. Complete missing gates within the authorized scope. Respect explicit exclusions without silently extending the task.
4. After each import or pricing change execute available customer-facing quote calculations for the captured rooms. Compare against source expectations. Record unavailable checks as pending.

## Scope and inventory before work

- File preparation produces checked files only. Any authorized hotel import/upload/update defaults to the complete profile review unless the user expressly limits it under the rule above. Preserve that narrower instruction in task evidence and describe the result accurately.
- Inventory every physical property in the requested sources, including collection members without prepared workbooks. Resolve combined headings before creating an identity. One resolved hotel gets one hotel folder and one owning catalog master; shared prices are not proof of shared identity.
- Keep the complete inventory separate from the selected upload set. Record every partial, blocked or excluded property and reason. Freeze the selected property and room keys from source review before writes; reconcile any later addition, removal or split explicitly rather than silently shrinking the expected set to match successes.
- Reuse requested languages from the session. If none were specified, use the established English/French/German upload convention. English fallback does not count as a translation.
Distinguish workbook readiness, catalog presence, saved rates, verified price cases and full-profile completion.

## Prepare and freeze each hotel packet

Before import, bind source editions, room aliases and capacities, requested locales, visually reviewed photos, year tags, PDF pages and pricing exceptions to the maintained workbook. Map returned hotel and room IDs immediately.

Check names against the room naming rules (see **Meister PDF to Contract**, Hotel occupancy, ages and missing places). An ordinary Triple, an extra bed and an extra guest are distinct concepts. Review descriptions against the actual room family or exclusive-property product, not just its occupancy alias. Description lengths and 2–3 photos remain targets; source-supported prose and an honestly documented photo fallback take priority over invented details.

Any later change to identity, names, translations, notes, photos, tags or attachments requires fresh **affected** MCP readback/delivery checks. Bind the completion ledger to the current packet. Existing pricing checks can be reused only with proof that the exact imported rates, financial fingerprint, subject IDs and applicable pricing-test inputs remain unchanged. A rename must reconcile the pricing workbook/display alias without silently replacing historical import evidence or changing capacities/prices.

A cover-image or translation change alone does not require repeating unaffected price calculations. Compare the relevant old/current components: identity/parent IDs, imported rates, pricing configuration and test inputs for financial checks; requested languages/content for locale checks; ordered assets for media checks; coverage/source mapping for tags and attachments. Catalog readback depends on the returned locale content, ordered media and delivered image bytes for that subject; it does not certify web-UI rendering. Preserve the original proof and save a current comparison receipt that references it and records what was unchanged; never relabel the old check as freshly executed or merely change its packet hash.

## Required evidence before full-profile completion

The table describes the evidence every applicable gate must have. For new or changed content, obtain it freshly. For unchanged content on an update, a current comparison receipt may bind the original substantive evidence to the final packet under the reuse rules above; “freshly read back” does not require downloading identical images or rewriting unchanged translations again. If the original evidence is missing, or current identity/content/media cannot be matched, obtain new evidence. Each selected hotel still has a gate result; preservation alone is not verification.

| Gate | Evidence required for every selected hotel |
| --- | --- |
| Identity | Source-bound physical hotel/location; captured hotel ID; every expected room alias, ID and capacity reconciled; no accidental merge or duplicate. |
| Rates | Canonical XLSX reopened and checked; delivered workbook bytes validated through MCP; raw live validator result retained; exact imported bytes and persisted price components reconciled. Existing-hotel top-ups use [scoped union validation](profile-upload.md#existing-hotel-add-new-rates-with-id), preserve earlier contracts and resolve overlaps/duplicates. Retain the exact evidence and applicable approved rule for accepted exceptions, including documented seasonal gaps and valid one-day seasons; an accepted exception is not a clean service pass or permission to ignore other failures. |
| Hotel content | One correctly spelled canonical hotel name, preserved untranslated; explicit nonblank description in each requested language, semantically reviewed and freshly read back. Hotel names do not require translated variants. |
| Room content | Every captured room has a correctly spelled canonical name and explicit nonblank translated names/descriptions in every requested language. Review meaning, room category and occupancy, not just filled fields; English fallback is not translation. Verify stored locale values on the same room IDs, preserving capacities and contract bindings. |
| Media | Ordered tenant-owned hotel and room photo IDs, first-image cover, provenance and visual review, or the exact [authorized no-photo exception](#authorized-scope-exceptions). Reuse physical-family images for variants; record truthful fallbacks. Never copy another tenant's stored media IDs. |
| Metadata | Year tags computed from actual rate coverage; lodge PDF includes the applicable pages from every used source and amendment, and its saved attachment filename is verified; existing unrelated fields/documents preserved. Live PDF verification remains filename-only, with no new download/content/hash/link requirement. |
| Notes | Read back concise consultant instructions for known pricing exceptions the saved rates cannot handle. If none apply, record the review privately. |
| Catalog verification | Read back every selected master and room through the customer’s MCP connection. Verify the identity, requested locales and media. |
| Pricing | Compare expected and actual buying costs, currency, selected rooms, traveler ages, season/board boundaries and ineligible cases. Record embedded errors. |
| Delivery | Reopen the lodge-specific source PDF, one final workbook with both sheets, and any optional notes in the customer’s chosen folder. Reconcile them with the catalog. |

Do not mark a gate verified from HTTP success, a worker's “done” message, aggregate counts or an unrelated/stale receipt. On interruption, reconcile current IDs and ledger before retrying; resume only pending work. Keep completed/pending counts visible. A missing required check is pending, not a pass. Catalog cleanup requires separate customer authorization.

After a blocker clears, [resume the upload](../catalog-workflow.md#resume-an-upload-after-a-blocker-clears) and apply this table to the resulting packet. Confirm that the previously held rows or steps now have evidence through saved-rate readback, applicable live price checks and delivery. Reuse unchanged gate evidence only under the comparison rules above.

## Authorized scope exceptions

An explicit instruction to import specified hotels or rooms without photos changes their media scope. Record the applicable user instruction, exact subject keys and reason privately before final validation. The media gate then reports an authorized exception, never `verified` images with an empty list. Do not infer this permission from unavailable pictures, a previous client's exception, a worker's decision or an unrelated rates-only request. Other properties retain normal media requirements.

Keep hotel notes dedicated to pricing exceptions. Missing-picture notices and work status stay in private evidence or the agreed review channel. Catalog readback still checks the no-photo profile's requested languages and content; it records no delivered images and cannot claim image-delivery checks. Report completion as complete within the authorized scope and disclose the media exception once in the handoff. An explicitly rates-only task remains a rates-only result rather than a full-profile claim.

### Explicit limited scope and language selection

Rates-only still requires hotel gates `identity`, `rates`, `source_documents`, `rate_year_tags`, `booking_notes`, `live_prices`, `publication`, and every selected room's `identity`. It excludes profile text/media checks; preserve those fields and disclose the exclusion. An explicit photo exception applies only to the specified properties or rooms. Record the customer's requested languages and the exact properties for any narrower language scope.

### Content and semantic-review receipts

Record the actual saved hotel name and description in every requested language. Preserve the same proper hotel name across language views. Check localized room names and descriptions for blanks, fallback and meaning.

Bind each room’s saved name, description and capacity to its original room and hotel IDs. Compare spelling, occupancy, room category and translated meaning against the source. Record which languages and fields were reviewed.

### Live calculation receipts

For each executed case save its source expectation, actual result and any discrepancy in private working evidence. For each changed hotel, verify a positive, source-priced stay for the intended rooms. Also test an ineligible date or party where applicable. An expected rejection establishes a boundary but cannot demonstrate that a valid stay prices correctly.

- `request` and `response`: saved JSON artifact references `{path, sha256}`.
- `source_expectation`: `source`, independent `calculation`, `expected_cost` and `currency`.
- `cost_path` and `currency_path`: JSON pointers into the response `body` selecting buying cost and its currency, not selling price.
- `comparison`: `actual_cost`, `expected_cost`, `currency`, and `outcome: "match"` only for exact equality.

For a resolved discrepancy, record the exact delta and cause, including rounding or an approved representation. Keep the independent expected total. Disclose material differences and leave unexplained amounts pending.

Reuse a prior buying-price check only for the same hotel and rooms when the underlying rates, currency, financial inputs and cases are demonstrably unchanged. Retain the original result and current comparison, including any differences. Re-run the affected cases after a change or when equivalence is uncertain.

Claim full-profile completion only after all selected hotels and rooms pass the applicable checks. Disclose authorized omissions, pricing checks still pending and skipped properties.
