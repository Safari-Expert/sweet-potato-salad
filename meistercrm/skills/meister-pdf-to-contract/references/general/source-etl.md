# Source documents to prepared rate workbooks

Use this workflow for every supported contract type. Follow the guide for each item type for its pricing model. Use this guide for extraction, provenance, conversion and delivery.

## Establish the conversion contract

First bind the client and local workspace under [client folder operations](client-folder-operations.md). Work only from that client's evidence; no other client's cache or source is an allowed fallback.

Identify the requested types, supplier period, nonresident/resident scope when relevant, target currency policy, current workbook sample, the [fresh live location reference](../location-reference/live-reference.md), and global versus existing-item import. Ask only for missing decisions that affect the output; continue extracting independent material while an answer is pending.

Interpret the source before transcribing it. A rate table may mix room costs, meal supplements, park entry, vehicle hire, and activities. Each belongs to its own model; a mixed PDF does not imply a mixed-schema import dataset. Maintain each distinct scope once under the XLSX policy below; do not automatically emit a CSV sibling.

Use the target template for field names, order, and serialization. Use the supplier/authority evidence for the commercial meaning. The template's example amounts, free bands, capacities, and dates are not universal business rules.

## Extract with traceable coverage

For hotel batches, use the [source inventory and PDF cache](../hotels/preparation-tools.md#1-inventory-and-cache-pdf-extraction) to reuse unchanged page extraction. Keep the following visual and semantic checks: a cache hit is not evidence that a contract was studied or is applicable to this client.

1. Inventory each source, its date/version, pages/sheets, and selected template. For a PDF, inspect whether it has real text or scanned images. Read scanned pages with OCR and verify the rendered original.
2. Extract text/tables. Visually check multi-column tables, merged headings, continuation pages, footnotes, decimal separators, season boundaries, superscripts, and rate labels. OCR uncertainty belongs in a working exception list, not a guessed cost.
3. Carry supplier sheet/page/row references into an intermediate ledger. Useful fields are source, locator, product, route/location/room, rate basis, currency, tax/inclusion basis, eligibility, pax/age bands, validity, interpretation status, and intended output row. These are working fields, not CSV columns.
4. Separate repeated page headers and prose from data. Join wrapped descriptions without joining adjacent products. Expand merged labels only over their actual table scope. Preserve meaningful zero, blank, unavailable, and not-applicable distinctions.
5. Read source footnotes and later human corrections together. A minimum participation age overrides a generic free-child pattern; a return flight is not implied by an outbound flight; a percent child discount must become an absolute cost only when its base is known.
6. Reconcile coverage: source products/rules considered, excluded with reasons, unresolved, and output rules. Recheck every critical price, date, route, and age boundary against its source. Do not call a selected-page extraction a complete supplier conversion.

For historical CSVs, a dialect guess from a short prefix can misread embedded doubled quotes in descriptions. Check the actual header, quoting and every parsed row width across the whole file before comparing fields; an inconsistent guessed parse is not proof that the original rows are malformed. Only independently evaluated effective formulas agreeing with their caches establish arithmetic consistency; caches alone do not. Neither proves supplier-policy or tariff correctness. For inherited XLSX shared groups, follow [saved-formula verification](schema-and-validation.md#saved-xlsx-formulas-must-survive-reopening).

Bind PDF amounts to the visible row and column headings before modelling them. Native text order can reverse neighbouring meal-plan columns even when every number is extracted correctly. Retain the page/table locator and a visually confirmed column map; correct values under the wrong board labels still produce an incorrect conversion.

Verify that a workbook preview preserves native cell values and text before using it as source evidence. A preview importer can recalculate formulas or alter labels despite a read-only workflow. When pixels disagree with native XML, formulas or original cached values, retain the exact cell, source hash and screenshot; quarantine the preview's amounts and labels and withdraw findings caused by rendering. Native fallback must explicitly disclose incomplete visual verification.

Successful whole-sheet rendering does not prove that every condition is legible: merged cells, fixed row heights and resized tall images can clip policy text. Recover visibility with targeted ranges or layout changes in a separate in-memory preview, preserving supplier bytes and reconciling displayed values against native cells before and after the changes. Record numeric preview precision differences separately from text/type changes; a rendered zero from an empty formula cache is not a supplier tariff. Keep unresolved clipping explicit.

Count parsed CSV data records separately from physical text lines: a quoted description can span several lines without creating additional rows. Retain logical record and physical line locators when reporting discrepancies. Across supplier editions, rebind each value to its actual header even when column counts match; a replaced room category or occupancy column makes positional reuse unsafe.

Inspect visible annotations, overwrites and strikethroughs against extracted text. Extraction can retain an obsolete amount underneath an annotation or a crossed-out clause. Preserve the underlying text, visible amendment, page and any uncertain amendment authority separately. In collection documents, apply named-property policies only to their stated properties instead of treating every shared-page condition as collection-wide.

## Location matching

Resolve each intended location from the customer’s connected catalog and canonical references using [location matching](../location-reference/live-reference.md).

A park activity belongs to its source-supported park; proximity to a town does not establish equivalent identity. Keep approved destination modelling distinct from actual site/fee jurisdiction. Do not include tenant, access or geometry payloads, or invent helper-ID columns in the selected import schema.

## Currency, discounts, and tax

Preserve the actual supplier currency. The older handbook's USD default is not permission to label local-currency amounts USD or overwrite a missing currency. Confirm ambiguous symbols such as `$` from the source context. Different masters can have different currencies; one master/location must be internally consistent (see shared validation).

Only convert currency when requested or already authorized for the task. Record source currency, target currency, rate source/date, direction, formula, and rounding in the working ledger. Use a current authoritative rate when a live rate is requested; never present a remembered rate as live. Convert every affected monetary field consistently, including hotel supplements and location overnight/camping charges. Use decimal arithmetic and retain calculation precision until the chosen currency/output rounding boundary. No extra FX columns in the import CSV.

For percentage discounts, distinguish “pays 75%” from “75% discount.” Record the base amount and resulting absolute cost. Do not multiply a flat group cost by every traveler or divide a per-person cost by group size unless the supplier rule calls for it.

Keep published cost, taxes, levies and inclusions explicit in the ledger. On non-location templates, `tax` represents a fractional Supplier VAT rate (18% → `0.18`). Keep monetary charges, TDL and departure fees out of that field. Apply the location template’s own fee rules.

### Tax and levy handling

For hotel preparation, apply [hotel VAT and country adjustments](../hotels.md#vat-country-adjustments-and-rounding). Apply the linked country policy where applicable and retain evidence for each adjustment. Do not use the superseded fixed-money or general non-VAT-fee formulas.

Keep a supplied hotel `tax` column at numeric `0`; country additions belong in monetary price fields, not master VAT. Preserve a selected template without that column. Other service types retain their task-specific source and tax instructions; a primary park or service tariff is not automatically a tax because a government authority supplies it. File preparation does not change live VAT settings or importer semantics, and a zero location `tax` field does not disable country tax settings.

## Corrections and date rollovers

When asked to correct a file, preserve unrelated fields and compare before/after by stable product/rule identity. Fix only the named columns or demonstrated invalid rules. Do not discard conflicting records just to remove duplicates.

A requested year rollover changes only the specified validity values; preserve month/day and other fields when the user says “same.” Handle leap-day collisions explicitly. Check that different seasons/years do not collapse into overlapping or differently priced duplicates. Extending a draft's dates does not establish supplier validity for the next year; state when supplier renewal is unverified.

## One maintained XLSX per scope

Maintain exactly two sheets, `Contracts` first and `Original` second. Use literal payable values on the first. Preserve source quotes, units, locators, calculations, TDL status and held evidence on the second. Update the same workbook in place.

- Apply approved regional adjustments once to the canonical workbook's final rate values. Do not keep a parallel `_revised.xlsx`, `_tdl_adjusted.xlsx`, matching CSV or copied rate worksheet for the same scope. Keep the original tariff and compact adjustment provenance sufficient to reproduce the calculation; a second full price grid is not required evidence.
- This policy changes future generation and maintenance. It does not by itself authorize deleting, consolidating or renaming existing files. If cleanup is explicitly requested, reconcile versions, comments, formulas, unique rows and source evidence before retiring any duplicate; never delete solely because two extensions share a basename.

## Write and deliver

Maintain and deliver the canonical XLSX under the policy above. Generate or edit a local working copy so helper-created temporary/backup files stay local, verify it, then publish only the final bytes to the same canonical client path under [client folder operations](client-folder-operations.md#keep-all-working-files-on-the-local-computer). When a temporary CSV is actually required for checking/import, write it with a CSV library, UTF-8 (BOM acceptable when needed by Excel), and the selected delimiter (normally comma for MeisterCRM). Quote commas/newlines/quotes correctly; never build rows by string concatenation. Apply the [current hotel output representation](schema-and-validation.md#current-hotel-output-representation), including ISO dates, literal text flags and the required AI column; retain `DD/MM/YYYY` where selected older non-hotel templates require it. Use plain numeric cells and genuine empty fields. Do not include a Markdown fence, title, row index, explanatory footer, or error columns.

Reopen the saved bytes and apply the [checking gates](checking-gates.md): exact header, row widths, counts and limits, reference matches, values, identities, conflict/coverage checks, and representative source-to-row mappings. Retain accepted closure/outlier exceptions in a separate report with source evidence and exact scope. A CSV opening in one Excel column can be a delimiter/locale issue: inspect the saved bytes and template before blaming the user or changing the schema.

Return the actual output file plus a short statement of what it contains and material unresolved/excluded rules. Keep interpretation notes and evidence out of import columns. Live import and supplier/catalog changes require their own task authorization; a successful offline preflight is not a successful import.
